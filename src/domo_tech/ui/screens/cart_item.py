"""Cart item widget used by the store screen."""

from __future__ import annotations

# Third-party
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class CartItem(Horizontal):
    """Fila de ítem en el carrito."""

    def __init__(self, name: str, qty: int, price: float, **kwargs):
        super().__init__(**kwargs, classes="cart-item")
        self._name = name
        self._qty = qty
        self._price = price

    def compose(self) -> ComposeResult:
        yield Static(self._name, classes="ci-name")
        yield Static(f"×{self._qty}", classes="ci-qty")
        yield Static(f"${self._price * self._qty:,.2f}", classes="ci-price")
