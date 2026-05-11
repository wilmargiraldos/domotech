"""
CYBER//STORE — Tienda cyberpunk en terminal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instalar:  pip install textual
Ejecutar:  python cyber_store.py

Usuarios de prueba:
  admin / 1234
  cyber / punk
"""

from __future__ import annotations
from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Input, Button, Static, DataTable, Footer
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding
from textual.reactive import reactive
from textual import on
from rich.text import Text
from datetime import datetime
from domo_tech.ui.screens.login import LoginScreen, DEFAULT_USERS
from domo_tech.ui.screens.store import StoreScreen
from domo_tech.ui.styles import CYBER_STORE_CSS

# ─── Datos ────────────────────────────────────────────────────────

PRODUCTS: list[dict[str, object]] = [
    {"id": 1, "name": "Neural Interface Mk.III", "price": 299.99, "cat": "Hardware",  "stock": 5},
    {"id": 2, "name": "Synth-Leather Jacket",    "price": 189.00, "cat": "Ropa",      "stock": 12},
    {"id": 3, "name": "Holo-Display 4K",         "price": 549.00, "cat": "Hardware",  "stock": 3},
    {"id": 4, "name": "EMP Shielder v2",          "price":  89.99, "cat": "Defensa",   "stock": 20},
    {"id": 5, "name": "CryptoKey Implant",        "price": 1200.0, "cat": "Implantes", "stock": 2},
    {"id": 6, "name": "Night Vision Contacts",    "price": 450.00, "cat": "Implantes", "stock": 8},
    {"id": 7, "name": "Data Spike Mk.II",         "price":  75.50, "cat": "Tools",     "stock": 15},
    {"id": 8, "name": "Neon Arm Sleeve",          "price":  35.00, "cat": "Ropa",      "stock": 30},
    {"id": 9, "name": "Quantum Firewall Chip",    "price": 875.00, "cat": "Hardware",  "stock": 4},
    {"id":10, "name": "Bio-Tracker Tattoo",       "price": 220.00, "cat": "Implantes", "stock": 7},
]

# ─── CSS ──────────────────────────────────────────────────────────

CSS = CYBER_STORE_CSS
USE_WIDE_LOGIN_BANNER = False

# ─── Pantallas ────────────────────────────────────────────────────


class CartItem(Horizontal):
    """Fila de ítem en el carrito."""
    def __init__(self, name: str, qty: int, price: float, **kwargs):
        super().__init__(**kwargs, classes="cart-item")
        self._name  = name
        self._qty   = qty
        self._price = price

    def compose(self) -> ComposeResult:
        yield Static(self._name, classes="ci-name")
        yield Static(f"×{self._qty}", classes="ci-qty")
        yield Static(f"${self._price * self._qty:,.2f}", classes="ci-price")


class StoreScreen(Screen):
    """Pantalla principal de la tienda."""

    BINDINGS = [
        Binding("a", "add_to_cart",  "Agregar"),
        Binding("q", "logout",       "Salir"),
        Binding("c", "checkout",     "Checkout"),
        Binding("x", "clear_cart",   "Vaciar carrito"),
    ]

    cart: reactive[dict] = reactive({})
    status_msg: reactive[str] = reactive("SISTEMA LISTO // NAVEGA CON ↑↓ // [A] AGREGAR // [C] CHECKOUT")

    def compose(self) -> ComposeResult:
        # Header
        with Horizontal(id="store-header"):
            yield Static("⬡  CYBER//STORE  ⬡", id="store-title")
            yield Static(f"[ {self.app.current_user.upper()}@NEXUS ]", id="user-badge")

        # Área principal
        with Horizontal(id="main-area"):
            # Panel productos
            with Vertical(id="products-panel"):
                with Horizontal(id="prod-header"):
                    yield Static("▸ CATÁLOGO DE PRODUCTOS", id="prod-header-title")
                    yield Input(placeholder="Filtrar...", id="filter-input")
                yield DataTable(id="products-table", cursor_type="row")
                with Horizontal(id="prod-actions"):
                    yield Button("⊕  AGREGAR AL CARRITO  [A]", id="btn-add")
                    yield Button("⏻  LOGOUT  [Q]", id="btn-logout")

            # Panel carrito
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

        # Status bar
        with Horizontal(id="status-bar"):
            yield Static(self.status_msg, id="status-text")
            yield Static("", id="clock")

    def on_mount(self) -> None:
        self._build_table(PRODUCTS)
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        now = datetime.utcnow().strftime("UTC %H:%M:%S")
        self.query_one("#clock", Static).update(now)

    # ── Tabla de productos ──────────────────────────────────────

    def _build_table(self, products: list) -> None:
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
            p for p in PRODUCTS
            if query in p["name"].lower() or query in p["cat"].lower()
        ]
        self._build_table(filtered)

    # ── Carrito ─────────────────────────────────────────────────

    def _get_selected_product(self):
        table = self.query_one("#products-table", DataTable)
        if table.row_count == 0:
            return None
        row_key = table.cursor_row
        # Obtener ID desde la celda de la fila
        try:
            cell_val = table.get_cell_at((row_key, 0))
            pid = int(str(cell_val))
            return next((p for p in PRODUCTS if p["id"] == pid), None)
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

        self.cart = dict(self.cart)  # Trigger reactivo
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
        self.app.current_user = ""
        self.app.pop_screen()

    def action_checkout(self) -> None:
        if not self.cart:
            self.status_msg = "⚠  EL CARRITO ESTÁ VACÍO"
            return
        self.app.push_screen(CheckoutModal(dict(self.cart), self._on_order_confirmed))

    def _on_order_confirmed(self) -> None:
        self.cart = {}
        self._refresh_cart_ui()
        self.status_msg = "✓  ORDEN PROCESADA"
        self.app.push_screen(SuccessModal())

    def _refresh_cart_ui(self) -> None:
        # Limpiar items
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
            p   = entry["product"]
            qty = entry["qty"]
            container.mount(CartItem(p["name"], qty, p["price"]))
            total += p["price"] * qty
            count += qty

        self.query_one("#cart-count", Static).update(f"{count} ítem{'s' if count > 1 else ''}")
        self.query_one("#total-value", Static).update(f"${total:,.2f}")


class CheckoutModal(ModalScreen):
    """Modal de resumen y confirmación de compra."""

    def __init__(self, cart: dict, on_confirm_callback, **kwargs):
        super().__init__(**kwargs)
        self._cart     = cart
        self._callback = on_confirm_callback

    def compose(self) -> ComposeResult:
        total = sum(e["product"]["price"] * e["qty"] for e in self._cart.values())
        with Container(id="checkout-box"):
            yield Static("◈  RESUMEN DE ORDEN  ◈", id="checkout-title")
            yield Static("━" * 40, id="checkout-divider")
            for entry in self._cart.values():
                p = entry["product"]
                with Horizontal(classes="checkout-row"):
                    yield Static(p["name"], classes="co-name")
                    yield Static(f"×{entry['qty']}", classes="co-qty")
                    yield Static(f"${p['price'] * entry['qty']:,.2f}", classes="co-sub")
            with Horizontal(id="checkout-total-row"):
                yield Static("TOTAL:", id="co-total-label")
                yield Static(f"${total:,.2f}", id="co-total-val")
            yield Static("⚡ TRANSACCIÓN ENCRIPTADA — RED SEGURA", id="checkout-warn")
            with Horizontal(id="checkout-btns"):
                yield Button("✓  CONFIRMAR ORDEN", id="btn-confirm")
                yield Button("✕  CANCELAR", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            self.dismiss()
            self._callback()
        elif event.button.id == "btn-cancel":
            self.dismiss()


class SuccessModal(ModalScreen):
    """Modal de confirmación de compra exitosa."""

    def compose(self) -> ComposeResult:
        import random
        order_id = f"NX-{random.randint(100000, 999999)}"
        with Container(id="success-box"):
            yield Static("▓▓▓  TRANSACCIÓN EXITOSA  ▓▓▓", id="success-icon")
            yield Static("Tu orden ha sido procesada y encriptada\nen la blockchain de NexusPay.", id="success-msg")
            yield Static(f"ORDEN # {order_id}", id="success-order")
            yield Button("⟫  VOLVER A LA TIENDA  ⟪", id="btn-ok")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ok":
            self.dismiss()


# ─── App ──────────────────────────────────────────────────────────

class CyberStore(App):
    CSS = CSS
    TITLE = "CYBER//STORE"

    current_user: str = ""

    def on_mount(self) -> None:
        self.push_screen(
            LoginScreen(
                on_login_success=lambda: self.push_screen(StoreScreen()),
                users=DEFAULT_USERS,
                use_wide_banner=USE_WIDE_LOGIN_BANNER,
            )
        )


def main() -> None:
    CyberStore().run()


if __name__ == "__main__":
    main()
