"""Main Store screen."""

from __future__ import annotations

# Standard library
from datetime import datetime
from typing import Any, Protocol, TypedDict, cast

# Third-party
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, DataTable, Input, Static

# Local
from domo_tech.ui.screens.cart_item import CartItem
from domo_tech.ui.screens.login import LoginScreen
from domo_tech.ui.screens.modals import (
    CheckoutModal,
    HelpModal,
    ProductDetailModal,
    SuccessModal,
)


class Product(TypedDict):
    id: int
    name: str
    price: float
    cat: str
    stock: int
    description: str
    features: list[str]
    specs: dict[str, str]


class CartEntry(TypedDict):
    product: Product
    qty: int


class InventoryProvider(Protocol):
    def list_products(self) -> list[Product]: ...

    def purchase(self, items: dict[int, int]) -> tuple[bool, str]: ...


class TraceProvider(Protocol):
    def record_sale(
        self,
        username: str,
        cart_entries: list[dict[str, Any]],
        user_id: int | None = None,
        user_role: str = "client",
    ) -> dict[str, Any]: ...

    def record_event(self, event_type: str, **details: Any) -> dict[str, Any]: ...
class StoreScreen(Screen[None]):
    """Pantalla principal de la tienda."""

    BINDINGS = [
        Binding("a", "add_to_cart", "Agregar"),
        Binding("q", "logout", "Salir"),
        Binding("c", "checkout", "Checkout"),
        Binding("x", "clear_cart", "Vaciar carrito"),
        Binding("v", "view_product", "Vista"),
        Binding("h", "show_help", "Ayuda"),
        Binding("f1", "show_help", "Ayuda"),
    ]

    cart: reactive[dict[int, CartEntry]] = reactive({})
    status_msg: reactive[str] = reactive(
        "SISTEMA LISTO // [F1/H] AYUDA // NAVEGA CON ↑↓ // [V] DETALLE // [A] AGREGAR // [C] CHECKOUT // [X] VACIAR // [Q] LOGOUT"
    )

    def __init__(
        self,
        products: list[Product] | None = None,
        inventory_store: InventoryProvider | None = None,
        trace_store: TraceProvider | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._products: list[Product] = list(products or [])
        self._inventory_store = inventory_store
        self._trace_store = trace_store
        self.cart = {}

    def compose(self) -> ComposeResult:
        app = cast(Any, self.app)
        current_user = str(getattr(app, "current_user", ""))

        with Horizontal(id="store-header"):
            yield Static(
                "⬡  DOMO-TECH - TIENDA ONLINE  ⬡",
                id="store-title",
                expand=True,
                markup=False,
            )
            yield Static(
                f"[ {current_user.upper()}@SOFTEDGE-LABS ]",
                id="user-badge",
                markup=False,
            )

        with Horizontal(id="main-area"):
            with Vertical(id="products-panel"):
                with Horizontal(id="prod-header"):
                    yield Static("▸ CATÁLOGO DE PRODUCTOS", id="prod-header-title")
                    yield Input(placeholder="Buscar por nombre...", id="filter-input")
                yield DataTable(id="products-table", cursor_type="row")
                with Horizontal(id="prod-actions"):
                    yield Button("⊕  AGREGAR AL CARRITO  [A]", id="btn-add")
                    yield Button("⏻  LOGOUT  [Q]", id="btn-logout")

            with Vertical(id="cart-panel"):
                with Horizontal(id="cart-header"):
                    yield Static("▸ CARRITO", id="cart-header-title")
                    yield Static("0 ítems", id="cart-count")
                with ScrollableContainer(id="cart-items", can_focus=False):
                    yield Static("[ CARRITO VACÍO ]", id="cart-empty")
                with Container(id="cart-footer"):
                    with Horizontal(id="total-row"):
                        yield Static("TOTAL:", id="total-label")
                        yield Static("$0.00", id="total-value")
                    yield Button("⟫  CHECKOUT  [C]", id="btn-checkout")
                    yield Button("✕  VACIAR  [X]", id="btn-clear")

        with Horizontal(id="status-bar"):
            yield Static(self.status_msg, id="status-text", expand=True, markup=False)
            yield Static("", id="clock", markup=False)

    def on_mount(self) -> None:
        self._build_table(self._products)
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        now = datetime.now().astimezone().strftime("%H:%M:%S")
        self.query_one("#clock", Static).update(now)

    def watch_status_msg(self, message: str) -> None:
        status_label = self.query_one_optional("#status-text", Static)
        if status_label is not None:
            status_label.update(message)

    def _build_table(self, products: list[Product]) -> None:
        table = self.query_one("#products-table", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "NOMBRE", "CATEGORÍA", "PRECIO", "STOCK")
        for p in products:
            stock_txt = Text(str(p["stock"]))
            if p["stock"] <= 3:
                stock_txt.stylize("bold red")
            elif p["stock"] <= 8:
                stock_txt.stylize("yellow")
            else:
                stock_txt.stylize("green")

            price_txt = Text(f"${p['price']:,.2f}", style="bold bright_yellow")
            table.add_row(
                str(p["id"]),
                p["name"],
                p["cat"],
                price_txt,
                stock_txt,
                key=str(p["id"]),
            )

    @on(Input.Changed, "#filter-input")
    def filter_products(self, event: Input.Changed) -> None:
        query = event.value.strip().lower()
        self._apply_product_filter(query)
        if not query:
            self.status_msg = "FILTRO LIMPIO // CATÁLOGO COMPLETO"
            return

        total = self.query_one("#products-table", DataTable).row_count
        self.status_msg = (
            f"FILTRO: {event.value} // {total} RESULTADO{'S' if total != 1 else ''}"
        )

    def _apply_product_filter(self, query: str | None = None) -> None:
        if query is None:
            query = self.query_one("#filter-input", Input).value.strip().lower()
        if not query:
            self._build_table(self._products)
            return

        filtered = [p for p in self._products if p["name"].lower().startswith(query)]
        self._build_table(filtered)

    def _get_selected_product(self) -> Product | None:
        table = self.query_one("#products-table", DataTable)
        if table.row_count == 0:
            return None
        row_key = table.cursor_row
        try:
            cell_val = table.get_cell_at(Coordinate(row_key, 0))
            pid = int(str(cell_val))
            return next((p for p in self._products if p["id"] == pid), None)
        except Exception:
            return None

    def action_add_to_cart(self) -> None:
        product = self._get_selected_product()
        if not product:
            self.status_msg = "⚠  SELECCIONA UN PRODUCTO PRIMERO"
            self._record_event("cart_add_failed_no_selection")
            return
        if product["stock"] <= 0:
            self.status_msg = f"✗  SIN STOCK: {product['name']}"
            self._record_event(
                "cart_add_failed_no_stock",
                product_id=product["id"],
                product_name=product["name"],
            )
            return
        pid = product["id"]
        if pid in self.cart:
            if self.cart[pid]["qty"] >= product["stock"]:
                self.status_msg = (
                    f"✗  STOCK INSUFICIENTE — SOLO {product['stock']} UNIDADES"
                )
                self._record_event(
                    "cart_add_failed_stock_limit",
                    product_id=product["id"],
                    product_name=product["name"],
                    stock=product["stock"],
                )
                return
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {"product": product, "qty": 1}

        self.cart = dict(self.cart)
        self.status_msg = f"✓  AGREGADO: {product['name']}"
        self._record_event(
            "cart_item_added",
            product_id=product["id"],
            product_name=product["name"],
            qty=self.cart[pid]["qty"],
        )
        self._refresh_cart_ui()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-add":
            self.action_add_to_cart()
        elif event.button.id == "btn-logout":
            self.action_logout()
        elif event.button.id == "btn-checkout":
            self.action_checkout()
        elif event.button.id == "btn-clear":
            self.action_clear_cart()

    def action_clear_cart(self) -> None:
        item_count = sum(entry["qty"] for entry in self.cart.values())
        self.cart = {}
        self._refresh_cart_ui()
        self.status_msg = "CARRITO VACIADO"
        self._record_event("cart_cleared", item_count=item_count)

    def action_view_product(self) -> None:
        product = self._get_selected_product()
        if not product:
            self.status_msg = "⚠  SELECCIONA UN PRODUCTO PARA VER DETALLE"
            return
        app = cast(Any, self.app)
        app.push_screen(ProductDetailModal(product))

    def action_show_help(self) -> None:
        app = cast(Any, self.app)
        app.push_screen(HelpModal())

    def action_logout(self) -> None:
        app = cast(Any, self.app)
        username = str(getattr(app, "current_user", ""))
        self._record_event("logout", username=username)
        self.cart = {}
        self._refresh_cart_ui()
        app.current_user = ""
        app.current_user_id = None
        app.current_user_role = ""
        login_screen = app.screen_stack[-2] if len(app.screen_stack) >= 2 else None
        if isinstance(login_screen, LoginScreen):
            login_screen.clear_form()
        app.pop_screen()

    def action_checkout(self) -> None:
        if not self.cart:
            self.status_msg = "⚠  EL CARRITO ESTÁ VACÍO"
            self._record_event("checkout_failed_empty_cart")
            return
        self._record_event(
            "checkout_started",
            item_count=sum(entry["qty"] for entry in self.cart.values()),
        )
        app = cast(Any, self.app)
        app.push_screen(CheckoutModal(dict(self.cart), self._on_order_confirmed))

    def _on_order_confirmed(self) -> None:
        items = {pid: entry["qty"] for pid, entry in self.cart.items()}
        success, message = self._commit_inventory_purchase(items)
        if not success:
            self.status_msg = f"✗  {message}"
            self._record_event("checkout_failed_inventory", message=message)
            self._reload_products()
            self._refresh_cart_ui()
            return

        sale = self._record_sale()
        self.cart = {}
        self._reload_products()
        self._clear_product_filter()
        self._refresh_cart_ui()
        order_id = str(sale.get("order_id", "DTWG-PENDIENTE"))
        self.status_msg = f"✓  ORDEN PROCESADA // {order_id} // {message}"
        app = cast(Any, self.app)
        app.push_screen(SuccessModal(order_id))

    def _commit_inventory_purchase(self, items: dict[int, int]) -> tuple[bool, str]:
        if self._inventory_store is not None:
            return self._inventory_store.purchase(items)

        products_by_id = {product["id"]: product for product in self._products}
        for product_id, qty in items.items():
            product = products_by_id.get(product_id)
            if product is None:
                return False, f"PRODUCTO {product_id} NO EXISTE"
            if product["stock"] < qty:
                return (
                    False,
                    f"STOCK INSUFICIENTE: {product['name']} ({product['stock']} DISPONIBLES)",
                )

        for product_id, qty in items.items():
            products_by_id[product_id]["stock"] -= qty
        return True, "INVENTARIO ACTUALIZADO"

    def _reload_products(self) -> None:
        if self._inventory_store is not None:
            self._products = self._inventory_store.list_products()
        self._apply_product_filter()

    def _record_sale(self) -> dict[str, Any]:
        app = cast(Any, self.app)
        username = str(getattr(app, "current_user", ""))
        user_id = getattr(app, "current_user_id", None)
        user_role = str(getattr(app, "current_user_role", "client") or "client")
        entries = [
            {"product": entry["product"], "qty": entry["qty"]}
            for entry in self.cart.values()
        ]
        if self._trace_store is not None:
            return self._trace_store.record_sale(
                username, entries, user_id=user_id, user_role=user_role
            )
        return {"order_id": f"DTWG-{datetime.now().strftime('%H%M%S')}"}

    def _record_event(self, event_type: str, **details: Any) -> None:
        if self._trace_store is not None:
            app = cast(Any, self.app)
            username = str(getattr(app, "current_user", ""))
            user_id = getattr(app, "current_user_id", None)
            user_role = str(getattr(app, "current_user_role", "") or "")
            if user_id is not None and "user_id" not in details:
                details["user_id"] = user_id
            if username and "username" not in details:
                details["username"] = username
            if user_role and "user_role" not in details:
                details["user_role"] = user_role
            self._trace_store.record_event(event_type, **details)

    def _clear_product_filter(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        filter_input.value = ""
        self._apply_product_filter("")

    def _refresh_cart_ui(self) -> None:
        container = self.query_one("#cart-items", ScrollableContainer)
        for item in container.query(".cart-item"):
            item.remove()

        empty = self.query_one("#cart-empty", Static)

        if not self.cart:
            empty.display = True
            self.query_one("#cart-count", Static).update("0 ítems")
            self.query_one("#total-value", Static).update("$0.00")
            return

        empty.display = False
        total = 0.0
        count = 0
        for entry in self.cart.values():
            p = entry["product"]
            qty = entry["qty"]
            container.mount(CartItem(p["name"], qty, p["price"]))
            total += p["price"] * qty
            count += qty

        self.query_one("#cart-count", Static).update(
            f"{count} ítem{'s' if count > 1 else ''}"
        )
        self.query_one("#total-value", Static).update(f"${total:,.2f}")
