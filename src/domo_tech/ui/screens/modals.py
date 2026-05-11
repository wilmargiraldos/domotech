"""Checkout and success modals for the store flow."""

from __future__ import annotations

from typing import Callable

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class CheckoutModal(ModalScreen):
    """Modal de resumen y confirmación de compra."""

    def __init__(self, cart: dict, on_confirm_callback: Callable[[], None], **kwargs):
        super().__init__(**kwargs)
        self._cart = cart
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
            yield Static(
                "Tu orden ha sido procesada y encriptada\nen la blockchain de NexusPay.",
                id="success-msg",
            )
            yield Static(f"ORDEN # {order_id}", id="success-order")
            yield Button("⟫  VOLVER A LA TIENDA  ⟪", id="btn-ok")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ok":
            self.dismiss()