"""Checkout and success modals for the store flow."""

from __future__ import annotations

from typing import Callable

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
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


class ProductDetailModal(ModalScreen):
    """Modal de vista previa técnica del producto seleccionado."""

    def __init__(self, product: dict, **kwargs):
        super().__init__(**kwargs)
        self._product = product

    def compose(self) -> ComposeResult:
        product = self._product
        stock = int(product["stock"])
        stock_text = "AGOTADO" if stock <= 0 else f"{stock} unidades"
        features = product.get("features") or ["Sin características registradas."]
        specs = product.get("specs") or {}

        with Container(id="product-detail-box"):
            yield Static("◈  VISTA PREVIA DE PRODUCTO  ◈", id="product-detail-title")
            yield Static(str(product["name"]), id="product-detail-name", markup=False)
            with Horizontal(id="product-detail-meta"):
                yield Static(f"CATEGORÍA: {product['cat']}", classes="pd-meta", markup=False)
                yield Static(f"PRECIO: ${product['price']:,.2f}", classes="pd-meta", markup=False)
                yield Static(f"STOCK: {stock_text}", classes="pd-meta", markup=False)
            with ScrollableContainer(id="product-detail-body"):
                yield Static(str(product.get("description") or "Sin descripción técnica registrada."), id="pd-desc")
                yield Static("CARACTERÍSTICAS", classes="pd-section")
                for feature in features:
                    yield Static(f"• {feature}", classes="pd-line", markup=False)
                yield Static("ESPECIFICACIONES", classes="pd-section")
                if specs:
                    for label, value in specs.items():
                        yield Static(f"{label}: {value}", classes="pd-line", markup=False)
                else:
                    yield Static("Sin especificaciones registradas.", classes="pd-line")
            yield Button("⟫  CERRAR  ⟪", id="btn-detail-close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-detail-close":
            self.dismiss()


class SuccessModal(ModalScreen):
    """Modal de confirmación de compra exitosa."""

    def compose(self) -> ComposeResult:
        import random

        order_id = f"DTWG-{random.randint(100000, 999999)}"
        with Container(id="success-box"):
            yield Static("▓▓▓  TRANSACCIÓN EXITOSA  ▓▓▓", id="success-icon")
            yield Static(
                "Tu orden ha sido procesada y encriptada\nen la blockchain de SoftEdge Labs PAY.",
                id="success-msg",
            )
            yield Static(f"ORDEN # {order_id}", id="success-order")
            yield Button("⟫  VOLVER A LA TIENDA  ⟪", id="btn-ok")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ok":
            self.dismiss()
