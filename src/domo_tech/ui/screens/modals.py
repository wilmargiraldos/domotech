"""Checkout and success modals for the store flow."""

from __future__ import annotations

# Standard library
from typing import Callable

# Third-party
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static

HELP_TOPICS = [
    {
        "title": "Navegación general",
        "keys": "↑↓ / TAB / ENTER",
        "body": [
            "Usa ↑↓ para moverte por el catálogo de productos.",
            "Usa TAB para recorrer controles interactivos.",
            "ENTER activa el control enfocado cuando aplica.",
        ],
    },
    {
        "title": "Buscar productos",
        "keys": "Filtro de catálogo",
        "body": [
            "Escribe en la caja de búsqueda para filtrar productos por inicio del nombre.",
            "Backspace borra caracteres; al limpiar el campo vuelve el catálogo completo.",
            "La barra de estado muestra el texto filtrado y la cantidad de resultados.",
        ],
    },
    {
        "title": "Vista previa",
        "keys": "V",
        "body": [
            "Selecciona un producto y presiona V para abrir su ficha técnica.",
            "La ficha muestra descripción, características, especificaciones, precio y stock.",
            "La vista previa no agrega productos al carrito.",
        ],
    },
    {
        "title": "Agregar al carrito",
        "keys": "A / botón Agregar",
        "body": [
            "Selecciona un producto y presiona A para agregar una unidad al carrito.",
            "No se permite agregar más unidades que las disponibles en stock.",
            "Los productos con stock 0 permanecen visibles, pero no pueden agregarse.",
        ],
    },
    {
        "title": "Carrito",
        "keys": "X / botón Vaciar",
        "body": [
            "El panel derecho muestra productos agregados, cantidades y subtotal por línea.",
            "Presiona X para vaciar completamente el carrito.",
            "El total se actualiza cada vez que agregas o retiras el contenido completo.",
        ],
    },
    {
        "title": "Checkout",
        "keys": "C / botón Checkout",
        "body": [
            "Presiona C para abrir el resumen de orden.",
            "Al confirmar, el inventario persistente descuenta el stock comprado.",
            "Después de una compra exitosa se limpia el filtro y vuelve el catálogo completo.",
        ],
    },
    {
        "title": "Sesión",
        "keys": "Q / botón Logout",
        "body": [
            "Presiona Q para cerrar sesión y volver a login.",
            "Al hacer logout se descarta el carrito actual.",
            "La pantalla de login limpia usuario, contraseña y errores visibles.",
        ],
    },
    {
        "title": "Ayuda",
        "keys": "F1 / H / ESC",
        "body": [
            "Presiona F1 o H para abrir esta ventana.",
            "Usa el buscador para filtrar temas por acción, tecla o palabra clave.",
            "Presiona ESC o el botón Cerrar para volver a la tienda.",
        ],
    },
]


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
            with ScrollableContainer(id="checkout-items-scroll", can_focus=False):
                for entry in self._cart.values():
                    p = entry["product"]
                    with Horizontal(classes="checkout-row"):
                        yield Static(p["name"], classes="co-name")
                        yield Static(f"×{entry['qty']}", classes="co-qty")
                        yield Static(
                            f"${p['price'] * entry['qty']:,.2f}", classes="co-sub"
                        )
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
                yield Static(
                    f"CATEGORÍA: {product['cat']}", classes="pd-meta", markup=False
                )
                yield Static(
                    f"PRECIO: ${product['price']:,.2f}", classes="pd-meta", markup=False
                )
                yield Static(f"STOCK: {stock_text}", classes="pd-meta", markup=False)
            with ScrollableContainer(id="product-detail-body"):
                yield Static(
                    str(
                        product.get("description")
                        or "Sin descripción técnica registrada."
                    ),
                    id="pd-desc",
                )
                yield Static("CARACTERÍSTICAS", classes="pd-section")
                for feature in features:
                    yield Static(f"• {feature}", classes="pd-line", markup=False)
                yield Static("ESPECIFICACIONES", classes="pd-section")
                if specs:
                    for label, value in specs.items():
                        yield Static(
                            f"{label}: {value}", classes="pd-line", markup=False
                        )
                else:
                    yield Static("Sin especificaciones registradas.", classes="pd-line")
            yield Button("⟫  CERRAR  ⟪", id="btn-detail-close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-detail-close":
            self.dismiss()


class HelpModal(ModalScreen):
    """Searchable in-app help for store shortcuts and workflows."""

    BINDINGS = [
        Binding("escape", "dismiss", "Cerrar"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="help-box"):
            yield Static("◈  AYUDA DE DOMO-TECH  ◈", id="help-title")
            yield Input(placeholder="Buscar tema, tecla o acción...", id="help-search")
            with ScrollableContainer(id="help-results"):
                pass
            yield Button("⟫  CERRAR  ⟪", id="btn-help-close")

    def on_mount(self) -> None:
        self._render_topics("")
        self.query_one("#help-search", Input).focus()

    @on(Input.Changed, "#help-search")
    def filter_help_topics(self, event: Input.Changed) -> None:
        self._render_topics(event.value)

    def action_dismiss(self) -> None:
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-help-close":
            self.dismiss()

    def _render_topics(self, query: str) -> None:
        results = self.query_one("#help-results", ScrollableContainer)
        for widget in results.query(".help-entry, .help-empty"):
            widget.remove()

        normalized_query = query.strip().lower()
        matches = [
            topic
            for topic in HELP_TOPICS
            if self._topic_matches(topic, normalized_query)
        ]

        if not matches:
            results.mount(Static("Sin temas encontrados.", classes="help-empty"))
            return

        for topic in matches:
            body = "\n".join(f"  - {line}" for line in topic["body"])
            content = f"{topic['title']}\nTeclas: {topic['keys']}\n{body}"
            results.mount(Static(content, classes="help-entry", markup=False))

    def _topic_matches(self, topic: dict, query: str) -> bool:
        if not query:
            return True
        searchable = " ".join(
            [
                str(topic["title"]),
                str(topic["keys"]),
                " ".join(str(line) for line in topic["body"]),
            ]
        ).lower()
        return query in searchable


class SuccessModal(ModalScreen):
    """Modal de confirmación de compra exitosa."""

    def __init__(self, order_id: str = "DTWG-PENDIENTE", **kwargs):
        super().__init__(**kwargs)
        self._order_id = order_id

    def compose(self) -> ComposeResult:
        with Container(id="success-box"):
            yield Static("▓▓▓  TRANSACCIÓN EXITOSA  ▓▓▓", id="success-icon")
            yield Static(
                "Tu orden ha sido procesada y encriptada\nen la blockchain de SoftEdge Labs PAY.",
                id="success-msg",
            )
            yield Static(f"ORDEN # {self._order_id}", id="success-order")
            yield Button("⟫  VOLVER A LA TIENDA  ⟪", id="btn-ok")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ok":
            self.dismiss()
