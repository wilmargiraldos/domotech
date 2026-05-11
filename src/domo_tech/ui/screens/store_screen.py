"""Main Store screen."""

from __future__ import annotations

from datetime import datetime
from typing import Any, TypedDict, cast

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, DataTable, Input, Static

class Product(TypedDict):
    id: int
    name: str
    price: float
    cat: str
    stock: int


class CartEntry(TypedDict):
    product: Product
    qty: int


from domo_tech.ui.screens.cart_item import CartItem
from domo_tech.ui.screens.modals import CheckoutModal, SuccessModal


class StoreScreen(Screen[None]):
    """Pantalla principal de la tienda."""

    BINDINGS = [
        Binding("a", "add_to_cart", "Agregar"),
        Binding("q", "logout", "Salir"),
        Binding("c", "checkout", "Checkout"),
        Binding("x", "clear_cart", "Vaciar carrito"),
    ]

    cart = reactive({})
    status_msg: reactive[str] = reactive(
        "SISTEMA LISTO // NAVEGA CON ↑↓ // [A] AGREGAR // [C] CHECKOUT"
    )

    def __init__(self, products: list[Product] | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._products: list[Product] = list(products or [])

    def compose(self) -> ComposeResult:
        app = cast(Any, self.app)
        current_user = str(getattr(app, "current_user", ""))

        with Horizontal(id="store-header"):
            yield Static("⬡  DOMO-TECH - TIENDA ONLINE  ⬡", id="store-title")
            yield Static(f"[ {current_user.upper()}@SOFTEDGE-LABS ]", id="user-badge")

        with Horizontal(id="main-area"):
            with Vertical(id="products-panel"):
                with Horizontal(id="prod-header"):
                    yield Static("▸ CATÁLOGO DE PRODUCTOS", id="prod-header-title")
                    yield Input(placeholder="Filtrar...", id="filter-input")
                yield DataTable(id="products-table", cursor_type="row")
                with Horizontal(id="prod-actions"):
                    yield Button("⊕  AGREGAR AL CARRITO  [A]", id="btn-add")
                    yield Button("⏻  LOGOUT  [Q]", id="btn-logout")

            with Vertical(id="cart-panel"):
                with Horizontal(id="cart-header"):
                    yield Static("▸ CARRITO", id="cart-header-title")
                    yield Static("0 ítems", id="cart-count")
                with ScrollableContainer(id="cart-items"):
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
        query = event.value.lower()
        filtered = [
            p for p in self._products if query in p["name"].lower() or query in p["cat"].lower()
        ]
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
            return
        pid = product["id"]
        if pid in self.cart:
            if self.cart[pid]["qty"] >= product["stock"]:
                self.status_msg = f"✗  STOCK INSUFICIENTE — SOLO {product['stock']} UNIDADES"
                return
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {"product": product, "qty": 1}

        self.cart = dict(self.cart)
        self.status_msg = f"✓  AGREGADO: {product['name']}"
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
        self.cart = {}
        self._refresh_cart_ui()
        self.status_msg = "CARRITO VACIADO"

    def action_logout(self) -> None:
        app = cast(Any, self.app)
        app.current_user = ""
        app.pop_screen()

    def action_checkout(self) -> None:
        if not self.cart:
            self.status_msg = "⚠  EL CARRITO ESTÁ VACÍO"
            return
        app = cast(Any, self.app)
        app.push_screen(CheckoutModal(dict(self.cart), self._on_order_confirmed))

    def _on_order_confirmed(self) -> None:
        self.cart = {}
        self._refresh_cart_ui()
        self.status_msg = "✓  ORDEN PROCESADA"
        app = cast(Any, self.app)
        app.push_screen(SuccessModal())

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

        self.query_one("#cart-count", Static).update(f"{count} ítem{'s' if count > 1 else ''}")
        self.query_one("#total-value", Static).update(f"${total:,.2f}")
