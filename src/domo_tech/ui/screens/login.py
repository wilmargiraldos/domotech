"""Login screen for Domo Tech.

This module isolates all UI and logic related to login so it can evolve
independently from the rest of the app screens.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static
from domo_tech.ui.branding import BANNER_ONE_ROW, BANNER_TWO_ROWS


DEFAULT_USERS = {
    "admin": "1234",
    "cyber": "punk",
    "user": "pass",
}


LOGIN_BANNER_DEFAULT = BANNER_TWO_ROWS.strip("\n")
LOGIN_BANNER_WIDE = BANNER_ONE_ROW.strip("\n")


class LoginScreen(Screen):
    """Pantalla de login con estética cyberpunk."""

    BINDINGS = [("enter", "submit", "Login")]

    def __init__(
        self,
        on_login_success: Callable[[], None],
        users: dict[str, str] | None = None,
        use_wide_banner: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._on_login_success = on_login_success
        self._users = users or DEFAULT_USERS
        self._use_wide_banner = use_wide_banner

    def _banner_text(self) -> str:
        return LOGIN_BANNER_WIDE if self._use_wide_banner else LOGIN_BANNER_DEFAULT

    def compose(self) -> ComposeResult:
        box_classes = "login-box-wide" if self._use_wide_banner else ""
        with Container(id="login-box", classes=box_classes):
            yield Static(self._banner_text(), id="logo", markup=False)
            yield Static("[ ACCESO RESTRINGIDO — INGRESA TUS CREDENCIALES ]", id="login-tag")
            yield Label("▸ USUARIO", classes="field-label")
            yield Input(placeholder="user@nexus.io", id="input-user")
            yield Label("▸ CONTRASEÑA", classes="field-label")
            yield Input(placeholder="••••••••", password=True, id="input-pass")
            yield Button("⟫  INICIAR SESIÓN  ⟪", id="btn-login")
            yield Static("", id="login-error")
            yield Static("v0.0.1 // DOMO-TECH // ACCESO AUTORIZADO REQUERIDO", id="login-footer-text")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-login":
            self._try_login()

    def action_submit(self) -> None:
        self._try_login()

    def clear_form(self) -> None:
        self.query_one("#input-user", Input).value = ""
        self.query_one("#input-pass", Input).value = ""
        self.query_one("#login-error", Static).update("")

    def _try_login(self) -> None:
        user = self.query_one("#input-user", Input).value.strip()
        pwd = self.query_one("#input-pass", Input).value.strip()
        err = self.query_one("#login-error", Static)

        if not user or not pwd:
            err.update("⚠  CAMPOS VACÍOS — INGRESA USUARIO Y CONTRASEÑA")
            self._record_event("login_validation_failed", username=user or "")
            return

        if self._users.get(user) == pwd:
            self.app.current_user = user
            self._record_event("login_success", username=user)
            self._on_login_success()
        else:
            err.update("✗  ACCESO DENEGADO — CREDENCIALES INVÁLIDAS")
            self.query_one("#input-pass", Input).value = ""
            self._record_event("login_failed", username=user)

    def _record_event(self, event_type: str, **details: Any) -> None:
        app = cast(Any, self.app)
        trace = getattr(app, "trace", None)
        if trace is not None:
            trace.record_event(event_type, **details)
