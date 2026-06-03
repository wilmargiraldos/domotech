"""Administrative dashboard for Domo Tech."""

from __future__ import annotations

# Standard library
import json
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Protocol, cast

# Third-party
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input, Static


class AdminUserStore(Protocol):
    def list_users(self) -> list[dict[str, Any]]: ...

    def update_user(
        self,
        user_id: int,
        *,
        username: str | None = None,
        password: str | None = None,
        role: str | None = None,
        active: bool | None = None,
    ) -> tuple[bool, str, dict[str, Any] | None]: ...

    def promote_to_admin(
        self, user_id: int
    ) -> tuple[bool, str, dict[str, Any] | None]: ...


class AdminInventoryStore(Protocol):
    def list_products(self) -> list[dict[str, Any]]: ...

    def update_product(
        self,
        product_id: int,
        *,
        name: str | None = None,
        price: float | None = None,
        cat: str | None = None,
        stock: int | None = None,
        description: str | None = None,
        features: list[str] | None = None,
        specs: dict[str, str] | None = None,
    ) -> tuple[bool, str, dict[str, Any] | None]: ...


class AdminTraceStore(Protocol):
    def list_sales(self) -> list[dict[str, Any]]: ...

    def list_events(self) -> list[dict[str, Any]]: ...

    def sales_summary(self) -> dict[str, Any]: ...

    def record_event(self, event_type: str, **details: Any) -> dict[str, Any]: ...


class AdminScreen(Screen[None]):
    """Hybrid cyberpunk dashboard for privileged operators."""

    BINDINGS = [
        Binding("q", "logout", "Salir"),
        Binding("escape", "logout", "Salir"),
        Binding("r", "refresh_data", "Refrescar"),
    ]

    def __init__(
        self,
        users_store: AdminUserStore,
        inventory_store: AdminInventoryStore,
        trace_store: AdminTraceStore,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._users_store = users_store
        self._inventory_store = inventory_store
        self._trace_store = trace_store
        self.section = "overview"
        self._users: list[dict[str, Any]] = []
        self._products: list[dict[str, Any]] = []
        self._sales: list[dict[str, Any]] = []
        self._events: list[dict[str, Any]] = []
        self._selected_user_id: int | None = None
        self._selected_product_id: int | None = None
        self._last_users_cursor = -1
        self._last_products_cursor = -1

    def compose(self) -> ComposeResult:
        with Container(id="admin-shell"):
            with Horizontal(id="admin-header"):
                yield Static(
                    "◈  PANEL ADMINISTRATIVO  ◈", id="admin-title", markup=False
                )
                yield Static("", id="admin-user", markup=False)

            with Horizontal(id="admin-nav"):
                yield Button("RESUMEN", id="admin-tab-overview")
                yield Button("USUARIOS", id="admin-tab-users")
                yield Button("PRODUCTOS", id="admin-tab-products")
                yield Button("VENTAS", id="admin-tab-sales")
                yield Button("LOGS", id="admin-tab-logs")

            with Horizontal(id="admin-kpis"):
                yield Static("", id="admin-kpi-users")
                yield Static("", id="admin-kpi-products")
                yield Static("", id="admin-kpi-sales")
                yield Static("", id="admin-kpi-events")

            with Container(id="admin-main"):
                yield Static("", id="admin-status")

                with Container(id="admin-content"):
                    yield from self._compose_overview_section()
                    yield from self._compose_users_section()
                    yield from self._compose_products_section()
                    yield from self._compose_sales_section()
                    yield from self._compose_logs_section()

            with Horizontal(id="admin-status-bar"):
                yield Static(
                    "BINDS: [Q/ESC] SALIR  [R] REFRESCAR  [↑↓] MOVERSE EN TABLAS  [TAB] NAVEGAR CONTROLES",
                    id="admin-help-text",
                    markup=False,
                )
                yield Static("", id="admin-op-status", markup=False)
                yield Static("", id="admin-clock", markup=False)

    def on_mount(self) -> None:
        self.refresh_data()
        self.set_interval(1, self._tick)
        self.set_interval(0.2, self._sync_selection_with_tables)
        self._set_status("TIP: USA ↑↓ EN TABLAS PARA ACTUALIZAR FORMULARIOS")

    def action_refresh_data(self) -> None:
        self.refresh_data()
        self._set_status("✓  DATOS ACTUALIZADOS")

    def action_logout(self) -> None:
        app = cast(Any, self.app)
        username = str(getattr(app, "current_user", ""))
        self._trace_store.record_event("logout", username=username, user_role="admin")
        app.current_user = ""
        app.current_user_id = None
        app.current_user_role = ""
        login_screen = app.screen_stack[-2] if len(app.screen_stack) >= 2 else None
        if login_screen is not None and hasattr(login_screen, "clear_form"):
            login_screen.clear_form()
        app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""
        if button_id == "admin-tab-overview":
            self._switch_section("overview")
        elif button_id == "admin-tab-users":
            self._switch_section("users")
        elif button_id == "admin-tab-products":
            self._switch_section("products")
        elif button_id == "admin-tab-sales":
            self._switch_section("sales")
        elif button_id == "admin-tab-logs":
            self._switch_section("logs")
        elif button_id == "admin-users-load":
            self._load_selected_user_form()
        elif button_id == "admin-users-save":
            self._save_user_changes()
        elif button_id == "admin-users-promote":
            self._promote_selected_user()
        elif button_id == "admin-users-toggle":
            self._toggle_selected_user_active()
        elif button_id == "admin-users-refresh":
            self.refresh_data()
        elif button_id == "admin-products-load":
            self._load_selected_product_form()
        elif button_id == "admin-products-save":
            self._save_product_changes()
        elif button_id == "admin-products-refresh":
            self.refresh_data()

    def refresh_data(self) -> None:
        self._update_header_user()
        self._users = self._users_store.list_users()
        self._products = self._inventory_store.list_products()
        self._sales = self._trace_store.list_sales()
        self._events = self._trace_store.list_events()
        self._update_kpis()
        self._render_overview_section()
        self._render_users_section()
        self._render_products_section()
        self._render_sales_section()
        self._render_logs_section()
        self._set_section_visibility(self.section)

    def _switch_section(self, section: str) -> None:
        self.section = section
        self._set_section_visibility(section)
        if section == "users":
            self._selected_user_id = None
            self._last_users_cursor = -1
            self._load_selected_user_form()
            self._set_status(
                "TIP: MUEVE EL CURSOR EN LA TABLA Y EL FORMULARIO SE ACTUALIZA AUTOMÁTICAMENTE"
            )
        elif section == "products":
            self._selected_product_id = None
            self._last_products_cursor = -1
            self._load_selected_product_form()
            self._set_status(
                "TIP: MUEVE EL CURSOR EN LA TABLA Y EL FORMULARIO SE ACTUALIZA AUTOMÁTICAMENTE"
            )
        elif section == "overview":
            self._render_overview_section()
        elif section == "sales":
            self._render_sales_section()
        elif section == "logs":
            self._render_logs_section()

    def _update_header_user(self) -> None:
        app = cast(Any, self.app)
        username = str(getattr(app, "current_user", ""))
        role = str(getattr(app, "current_user_role", "admin") or "admin")
        badge = f"{role.upper()} :: {username}" if username else role.upper()
        self.query_one("#admin-user", Static).update(badge)

    def _tick(self) -> None:
        now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
        clock = self.query_one_optional("#admin-clock", Static)
        if clock is not None:
            clock.update(now)

    def _sync_selection_with_tables(self) -> None:
        if self.section == "users":
            users_table = self.query_one_optional("#admin-users-table", DataTable)
            if users_table is None:
                return
            try:
                row = int(users_table.cursor_row)
            except Exception:
                return
            if row != self._last_users_cursor and 0 <= row < len(self._users):
                self._last_users_cursor = row
                self._selected_user_id = int(self._users[row]["id"])
                self._load_selected_user_form()
        elif self.section == "products":
            products_table = self.query_one_optional("#admin-products-table", DataTable)
            if products_table is None:
                return
            try:
                row = int(products_table.cursor_row)
            except Exception:
                return
            if row != self._last_products_cursor and 0 <= row < len(self._products):
                self._last_products_cursor = row
                self._selected_product_id = int(self._products[row]["id"])
                self._load_selected_product_form()

    def _update_kpis(self) -> None:
        total_users = len(self._users)
        admin_count = sum(
            1 for user in self._users if str(user.get("role", "client")) == "admin"
        )
        low_stock = sum(
            1 for product in self._products if int(product.get("stock", 0)) <= 8
        )
        summary = self._trace_store.sales_summary()

        self.query_one("#admin-kpi-users", Static).update(
            f"USUARIOS\n{total_users} total // {admin_count} admins"
        )
        self.query_one("#admin-kpi-products", Static).update(
            f"INVENTARIO\n{len(self._products)} productos // {low_stock} bajo stock"
        )
        self.query_one("#admin-kpi-sales", Static).update(
            f"VENTAS\n{summary['sales_count']} órdenes // ${float(summary['total_revenue']):,.2f}"
        )
        self.query_one("#admin-kpi-events", Static).update(
            f"LOGS\n{len(self._events)} eventos registrados"
        )

    def _set_section_visibility(self, section: str) -> None:
        for section_id in (
            "#admin-overview-section",
            "#admin-users-section",
            "#admin-products-section",
            "#admin-sales-section",
            "#admin-logs-section",
        ):
            widget = self.query_one(section_id, Widget)
            widget.display = False

        visible_map = {
            "overview": "#admin-overview-section",
            "users": "#admin-users-section",
            "products": "#admin-products-section",
            "sales": "#admin-sales-section",
            "logs": "#admin-logs-section",
        }
        self.query_one(
            visible_map.get(section, "#admin-overview-section"), Widget
        ).display = True
        self._sync_nav_status(section)

    def _sync_nav_status(self, section: str) -> None:
        labels = {
            "overview": "RESUMEN",
            "users": "USUARIOS",
            "products": "PRODUCTOS",
            "sales": "VENTAS",
            "logs": "LOGS",
        }
        self.query_one("#admin-status", Static).update(
            f"SECCIÓN ACTIVA // {labels.get(section, 'RESUMEN')}"
        )

    def _compose_overview_section(self) -> ComposeResult:
        with ScrollableContainer(id="admin-overview-section"):
            yield Static("", id="admin-overview-text", markup=False)
            yield Static("", id="admin-sales-chart", markup=False)
            yield Static("", id="admin-top-products-chart", markup=False)
            yield Static("", id="admin-inventory-chart", markup=False)
            yield Static("", id="admin-events-chart", markup=False)
            yield Static("", id="admin-low-stock", markup=False)

    def _render_overview_section(self) -> None:
        self.query_one("#admin-overview-text", Static).update(
            self._build_overview_text()
        )
        self.query_one("#admin-sales-chart", Static).update(
            self._build_bar_series("VENTAS POR DÍA", self._sales_by_day(), width=28)
        )
        self.query_one("#admin-top-products-chart", Static).update(
            self._build_bar_series("TOP PRODUCTOS", self._top_products(), width=28)
        )
        self.query_one("#admin-inventory-chart", Static).update(
            self._build_bar_series(
                "INVENTARIO POR CATEGORÍA", self._inventory_by_category(), width=28
            )
        )
        self.query_one("#admin-events-chart", Static).update(
            self._build_bar_series(
                "ACTIVIDAD DE LOGS", self._event_type_counts(), width=28
            )
        )
        self.query_one("#admin-low-stock", Static).update(self._build_low_stock_lines())

    def _compose_users_section(self) -> ComposeResult:
        with ScrollableContainer(id="admin-users-section"):
            with Horizontal(id="admin-users-layout"):
                with Container(id="admin-users-table-box"):
                    yield Static("USUARIOS REGISTRADOS", classes="admin-section-title")
                    yield Static(
                        "Mueve el cursor con ↑↓ para cargar datos en el formulario.",
                        id="admin-users-hint",
                        markup=False,
                    )
                    yield DataTable(id="admin-users-table", cursor_type="row")
                    yield Button("CARGAR SELECCIÓN", id="admin-users-load")
                    yield Button("REFRESCAR", id="admin-users-refresh")

                with ScrollableContainer(id="admin-user-editor"):
                    yield Static("EDITAR USUARIO", classes="admin-section-title")
                    yield Static("Usuario", classes="admin-field-label")
                    yield Input(id="admin-user-username")
                    yield Static("Rol", classes="admin-field-label")
                    yield Input(id="admin-user-role")
                    yield Static("Nueva contraseña", classes="admin-field-label")
                    yield Input(id="admin-user-password", password=True)
                    yield Static("", id="admin-user-active-label", markup=False)
                    yield Button("GUARDAR CAMBIOS", id="admin-users-save")
                    yield Button("PROMOVER A ADMIN", id="admin-users-promote")
                    yield Button("TOGGLE ACTIVO", id="admin-users-toggle")

    def _render_users_section(self) -> None:
        self._populate_users_table()
        self._load_selected_user_form()

    def _compose_products_section(self) -> ComposeResult:
        with ScrollableContainer(id="admin-products-section"):
            with Horizontal(id="admin-products-layout"):
                with Container(id="admin-products-table-box"):
                    yield Static("PRODUCTOS", classes="admin-section-title")
                    yield Static(
                        "Mueve el cursor con ↑↓ para cargar datos en el formulario.",
                        id="admin-products-hint",
                        markup=False,
                    )
                    yield DataTable(id="admin-products-table", cursor_type="row")
                    yield Button("CARGAR SELECCIÓN", id="admin-products-load")
                    yield Button("REFRESCAR", id="admin-products-refresh")

                with ScrollableContainer(id="admin-product-editor"):
                    yield Static("EDITAR PRODUCTO", classes="admin-section-title")
                    yield Static("Nombre", classes="admin-field-label")
                    yield Input(id="admin-product-name")
                    yield Static("Categoría", classes="admin-field-label")
                    yield Input(id="admin-product-cat")
                    yield Static("Precio", classes="admin-field-label")
                    yield Input(id="admin-product-price")
                    yield Static("Stock", classes="admin-field-label")
                    yield Input(id="admin-product-stock")
                    yield Static("Descripción", classes="admin-field-label")
                    yield Input(id="admin-product-description")
                    yield Static(
                        "Características (; separado)", classes="admin-field-label"
                    )
                    yield Input(id="admin-product-features")
                    yield Static("Specs JSON", classes="admin-field-label")
                    yield Input(id="admin-product-specs")
                    yield Button("GUARDAR PRODUCTO", id="admin-products-save")

    def _render_products_section(self) -> None:
        self._populate_products_table()
        self._load_selected_product_form()

    def _compose_sales_section(self) -> ComposeResult:
        with ScrollableContainer(id="admin-sales-section"):
            yield Static("", id="admin-sales-overview", markup=False)
            yield Static("", id="admin-order-status-chart", markup=False)
            yield Static("", id="admin-revenue-chart", markup=False)

    def _render_sales_section(self) -> None:
        self.query_one("#admin-sales-overview", Static).update(
            self._build_sales_overview_text()
        )
        self.query_one("#admin-order-status-chart", Static).update(
            self._build_bar_series(
                "ORDENES POR ESTADO", self._order_status_counts(), width=32
            )
        )
        self.query_one("#admin-revenue-chart", Static).update(
            self._build_bar_series(
                "INGRESOS DIARIOS", self._sales_by_day(value_mode="revenue"), width=32
            )
        )

    def _compose_logs_section(self) -> ComposeResult:
        with ScrollableContainer(id="admin-logs-section"):
            yield Static("LOGS OPERATIVOS", classes="admin-section-title")
            with ScrollableContainer(id="admin-log-scroll"):
                pass

    def _render_logs_section(self) -> None:
        log_container = self.query_one("#admin-log-scroll", ScrollableContainer)
        for widget in list(log_container.children):
            widget.remove()
        for line in self._recent_event_lines(limit=120):
            log_container.mount(Static(line, markup=False))

    def _populate_users_table(self) -> None:
        table = self.query_one("#admin-users-table", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "USUARIO", "ROL", "ACTIVO", "CREADO")
        for user in self._users:
            table.add_row(
                str(user["id"]),
                str(user["username"]),
                str(user.get("role", "client")),
                "SI" if user.get("active", True) else "NO",
                str(user.get("created_at", ""))[:19],
                key=str(user["id"]),
            )

    def _populate_products_table(self) -> None:
        table = self.query_one("#admin-products-table", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "NOMBRE", "CATEGORÍA", "PRECIO", "STOCK")
        for product in self._products:
            table.add_row(
                str(product["id"]),
                str(product["name"]),
                str(product["cat"]),
                f"${float(product['price']):,.2f}",
                str(product["stock"]),
                key=str(product["id"]),
            )

    def _load_selected_user_form(self) -> None:
        user = self._selected_user()
        if user is None:
            self._selected_user_id = None
            self.query_one("#admin-user-username", Input).value = ""
            self.query_one("#admin-user-role", Input).value = ""
            self.query_one("#admin-user-password", Input).value = ""
            self.query_one("#admin-user-active-label", Static).update(
                "Sin usuario seleccionado"
            )
            return

        self._selected_user_id = int(user["id"])
        self.query_one("#admin-user-username", Input).value = str(
            user.get("username", "")
        )
        self.query_one("#admin-user-role", Input).value = str(
            user.get("role", "client")
        )
        self.query_one("#admin-user-password", Input).value = ""
        active_text = "ACTIVO" if user.get("active", True) else "INACTIVO"
        self.query_one("#admin-user-active-label", Static).update(
            f"Estado actual: {active_text}"
        )

    def _load_selected_product_form(self) -> None:
        product = self._selected_product()
        if product is None:
            self._selected_product_id = None
            for field_id in (
                "#admin-product-name",
                "#admin-product-cat",
                "#admin-product-price",
                "#admin-product-stock",
                "#admin-product-description",
                "#admin-product-features",
                "#admin-product-specs",
            ):
                self.query_one(field_id, Input).value = ""
            return

        self._selected_product_id = int(product["id"])
        self.query_one("#admin-product-name", Input).value = str(
            product.get("name", "")
        )
        self.query_one("#admin-product-cat", Input).value = str(product.get("cat", ""))
        self.query_one("#admin-product-price", Input).value = str(
            product.get("price", 0.0)
        )
        self.query_one("#admin-product-stock", Input).value = str(
            product.get("stock", 0)
        )
        self.query_one("#admin-product-description", Input).value = str(
            product.get("description", "")
        )
        self.query_one("#admin-product-features", Input).value = "; ".join(
            str(item) for item in product.get("features", [])
        )
        self.query_one("#admin-product-specs", Input).value = json.dumps(
            product.get("specs", {}), ensure_ascii=False
        )

    def _save_user_changes(self) -> None:
        user = self._selected_user()
        if user is None:
            self._set_status("⚠  SELECCIONA UN USUARIO PRIMERO")
            return

        username = self.query_one("#admin-user-username", Input).value.strip()
        role = self.query_one("#admin-user-role", Input).value.strip().lower()
        password = self.query_one("#admin-user-password", Input).value

        if role and role not in {"admin", "client"}:
            self._set_status("✗  EL ROL DEBE SER admin O client")
            return

        success, message, _ = self._users_store.update_user(
            int(user["id"]),
            username=username or None,
            password=password or None,
            role=role or None,
        )
        if not success:
            self._set_status(f"✗  {message}")
            return

        self._trace_store.record_event(
            "admin_user_updated",
            user_id=int(user["id"]),
            username=username or str(user.get("username", "")),
            user_role=role or str(user.get("role", "client")),
        )
        self._set_status(f"✓  {message}")
        self.refresh_data()
        self._select_user_by_id(int(user["id"]))

    def _promote_selected_user(self) -> None:
        user = self._selected_user()
        if user is None:
            self._set_status("⚠  SELECCIONA UN USUARIO PRIMERO")
            return

        success, message, _ = self._users_store.promote_to_admin(int(user["id"]))
        if not success:
            self._set_status(f"✗  {message}")
            return

        self._trace_store.record_event(
            "admin_user_promoted",
            user_id=int(user["id"]),
            username=str(user.get("username", "")),
        )
        self._set_status(f"✓  {message}")
        self.refresh_data()
        self._select_user_by_id(int(user["id"]))

    def _toggle_selected_user_active(self) -> None:
        user = self._selected_user()
        if user is None:
            self._set_status("⚠  SELECCIONA UN USUARIO PRIMERO")
            return

        new_active = not bool(user.get("active", True))
        success, message, _ = self._users_store.update_user(
            int(user["id"]), active=new_active
        )
        if not success:
            self._set_status(f"✗  {message}")
            return

        self._trace_store.record_event(
            "admin_user_active_toggled",
            user_id=int(user["id"]),
            username=str(user.get("username", "")),
            active=new_active,
        )
        self._set_status(f"✓  {message}")
        self.refresh_data()
        self._select_user_by_id(int(user["id"]))

    def _save_product_changes(self) -> None:
        product = self._selected_product()
        if product is None:
            self._set_status("⚠  SELECCIONA UN PRODUCTO PRIMERO")
            return

        name = self.query_one("#admin-product-name", Input).value.strip()
        category = self.query_one("#admin-product-cat", Input).value.strip()
        price_text = self.query_one("#admin-product-price", Input).value.strip()
        stock_text = self.query_one("#admin-product-stock", Input).value.strip()
        description = self.query_one("#admin-product-description", Input).value.strip()
        features_text = self.query_one("#admin-product-features", Input).value.strip()
        specs_text = self.query_one("#admin-product-specs", Input).value.strip()

        try:
            price = (
                float(price_text) if price_text else float(product.get("price", 0.0))
            )
            stock = int(stock_text) if stock_text else int(product.get("stock", 0))
        except ValueError:
            self._set_status("✗  PRECIO O STOCK INVÁLIDO")
            return

        features = self._parse_features(features_text) if features_text else None
        specs = self._parse_specs(specs_text) if specs_text else None
        if specs_text and specs is None:
            self._set_status("✗  SPECS JSON INVÁLIDO")
            return

        success, message, _ = self._inventory_store.update_product(
            int(product["id"]),
            name=name or None,
            price=price,
            cat=category or None,
            stock=stock,
            description=description or None,
            features=features,
            specs=specs,
        )
        if not success:
            self._set_status(f"✗  {message}")
            return

        self._trace_store.record_event(
            "admin_product_updated",
            product_id=int(product["id"]),
            product_name=name or str(product.get("name", "")),
            stock=stock,
        )
        self._set_status(f"✓  {message}")
        self.refresh_data()
        self._select_product_by_id(int(product["id"]))

    def _selected_user(self) -> dict[str, Any] | None:
        if self._selected_user_id is not None:
            return next(
                (
                    user
                    for user in self._users
                    if int(user["id"]) == self._selected_user_id
                ),
                None,
            )
        if not self._users:
            return None
        row = self._table_cursor_row("#admin-users-table")
        if row >= len(self._users):
            row = 0
        return self._users[row]

    def _selected_product(self) -> dict[str, Any] | None:
        if self._selected_product_id is not None:
            return next(
                (
                    product
                    for product in self._products
                    if int(product["id"]) == self._selected_product_id
                ),
                None,
            )
        if not self._products:
            return None
        row = self._table_cursor_row("#admin-products-table")
        if row >= len(self._products):
            row = 0
        return self._products[row]

    def _select_user_by_id(self, user_id: int) -> None:
        self._selected_user_id = user_id
        self._load_selected_user_form()

    def _select_product_by_id(self, product_id: int) -> None:
        self._selected_product_id = product_id
        self._load_selected_product_form()

    def _table_cursor_row(self, table_selector: str) -> int:
        table = self.query_one(table_selector, DataTable)
        try:
            return int(table.cursor_row)
        except Exception:
            return 0

    def _parse_features(self, text: str) -> list[str]:
        parts = [part.strip() for part in text.replace("\n", ";").split(";")]
        return [part for part in parts if part]

    def _parse_specs(self, text: str) -> dict[str, str] | None:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict):
            return None
        return {str(key): str(value) for key, value in payload.items()}

    def _build_overview_text(self) -> str:
        admin_count = sum(
            1 for user in self._users if str(user.get("role", "client")) == "admin"
        )
        client_count = len(self._users) - admin_count
        low_stock = [
            product for product in self._products if int(product.get("stock", 0)) <= 8
        ]
        return (
            "RESUMEN EJECUTIVO\n"
            f"Usuarios activos: {sum(1 for user in self._users if user.get('active', True))} | Admins: {admin_count} | Clientes: {client_count}\n"
            f"Productos: {len(self._products)} | Bajo stock: {len(low_stock)} | Ventas registradas: {len(self._sales)}\n"
        )

    def _build_sales_overview_text(self) -> str:
        summary = self._trace_store.sales_summary()
        return (
            "VENTAS Y RESUMEN\n"
            f"Órdenes completadas: {summary['sales_count']}\n"
            f"Ingresos acumulados: ${float(summary['total_revenue']):,.2f}\n"
            f"Unidades vendidas: {summary['total_items']}\n"
        )

    def _build_low_stock_lines(self) -> str:
        low_stock = [
            product for product in self._products if int(product.get("stock", 0)) <= 8
        ]
        if not low_stock:
            return "SIN ALERTAS DE STOCK BAJO"
        lines = ["ALERTAS DE STOCK BAJO"]
        for product in sorted(low_stock, key=lambda item: int(item.get("stock", 0))):
            lines.append(f"• {product['name']} — {product['stock']} unidades")
        return "\n".join(lines)

    def _sales_by_day(self, value_mode: str = "revenue") -> list[tuple[str, float]]:
        grouped: dict[str, float] = defaultdict(float)
        for sale in self._sales:
            timestamp = str(sale.get("timestamp", ""))
            try:
                day = datetime.fromisoformat(timestamp).date().isoformat()
            except ValueError:
                day = timestamp[:10] or "desconocido"
            if value_mode == "revenue":
                grouped[day] += float(sale.get("total", 0.0))
            else:
                grouped[day] += 1
        return sorted(grouped.items())

    def _top_products(self) -> list[tuple[str, float]]:
        totals: dict[str, float] = defaultdict(float)
        for sale in self._sales:
            for item in sale.get("items", []):
                totals[str(item.get("name", "Producto"))] += float(item.get("qty", 0))
        return sorted(totals.items(), key=lambda pair: pair[1], reverse=True)[:10]

    def _inventory_by_category(self) -> list[tuple[str, float]]:
        totals: dict[str, float] = defaultdict(float)
        for product in self._products:
            totals[str(product.get("cat", "Sin categoría"))] += float(
                product.get("stock", 0)
            )
        return sorted(totals.items(), key=lambda pair: pair[1], reverse=True)

    def _event_type_counts(self) -> list[tuple[str, float]]:
        counter = Counter(
            str(event.get("event_type", "unknown")) for event in self._events
        )
        return sorted(counter.items(), key=lambda pair: pair[1], reverse=True)

    def _order_status_counts(self) -> list[tuple[str, float]]:
        counter = Counter(str(sale.get("status", "completed")) for sale in self._sales)
        return sorted(counter.items(), key=lambda pair: pair[1], reverse=True)

    def _recent_event_lines(self, limit: int = 100) -> list[str]:
        events = self._events[-limit:]
        lines: list[str] = []
        for event in reversed(events):
            timestamp = str(event.get("timestamp", ""))
            event_type = str(event.get("event_type", "unknown"))
            details = event.get("details", {})
            lines.append(
                f"{timestamp}  |  {event_type}  |  {json.dumps(details, ensure_ascii=False)}"
            )
        return lines or ["SIN EVENTOS REGISTRADOS"]

    def _build_bar_series(
        self, title: str, pairs: list[tuple[str, float]], width: int = 24
    ) -> str:
        if not pairs:
            return f"{title}\nSIN DATOS\n"
        max_value = max(value for _, value in pairs) or 1
        lines = [title]
        for label, value in pairs[:10]:
            bar_length = max(1, int((value / max_value) * width)) if value > 0 else 0
            bar = "█" * bar_length if bar_length > 0 else "-"
            lines.append(
                f"{label[:24].ljust(24)} {bar} {value:.0f}"
                if float(value).is_integer()
                else f"{label[:24].ljust(24)} {bar} {value:.2f}"
            )
        return "\n".join(lines)

    def _set_status(self, message: str) -> None:
        self.query_one("#admin-op-status", Static).update(message)
