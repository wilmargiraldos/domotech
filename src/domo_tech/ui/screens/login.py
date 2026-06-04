"""Login screen for Domo Tech.

This module isolates all UI and logic related to login so it can evolve
independently from the rest of the app screens.
"""

from __future__ import annotations

# Standard library
from collections.abc import Callable
from typing import Any, Protocol, cast

# Third-party
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Input, Label, Static

# Local
from domo_tech.ui.branding import BANNER_ONE_ROW, BANNER_TWO_ROWS
from domo_tech.users import UserStore
from domo_tech.utils import read_project_meta as _read_project_meta


class UserProvider(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None: ...

    def register_client(
        self, username: str, password: str
    ) -> tuple[bool, str, dict | None]: ...


LOGIN_BANNER_DEFAULT = BANNER_TWO_ROWS.strip("\n")
LOGIN_BANNER_WIDE = BANNER_ONE_ROW.strip("\n")


class LoginScreen(Screen):
    """Pantalla de login con estética cyberpunk."""

    BINDINGS = [
        ("enter", "submit", "Login"),
        ("escape", "quit", "Salir"),
    ]

    def __init__(
        self,
        on_login_success: Callable[[], None],
        user_store: UserProvider | None = None,
        use_wide_banner: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._on_login_success = on_login_success
        self._user_store = user_store or UserStore()
        self._use_wide_banner = use_wide_banner

    def _banner_text(self) -> str:
        return LOGIN_BANNER_WIDE if self._use_wide_banner else LOGIN_BANNER_DEFAULT

    def compose(self) -> ComposeResult:
        box_classes = "login-box-wide" if self._use_wide_banner else ""
        with Container(id="login-box", classes=box_classes):
            yield Static(self._banner_text(), id="logo", markup=False)
            # yield Static("[ ACCESO RESTRINGIDO — INGRESA TUS CREDENCIALES ]", id="login-tag")
            yield Label("▸ USUARIO", classes="field-label")
            yield Input(placeholder="user@softedge-labs.com", id="input-user")
            yield Label("▸ CONTRASEÑA", classes="field-label")
            yield Input(placeholder="••••••••", password=True, id="input-pass")
            with Horizontal(id="login-actions"):
                yield Button("⟫  INICIAR SESIÓN  ⟪", id="btn-login")
                yield Button("CREAR CUENTA", id="btn-register")
                yield Button("SALIR", id="btn-exit")
            yield Static("", id="login-error")
            name, version = _read_project_meta()
            name = name.upper() if name else "DOMO-TECH"
            yield Static(
                f"v{version} // {name} // ACCESO AUTORIZADO REQUERIDO",
                id="login-footer-text",
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-login":
            self._try_login()
        elif event.button.id == "btn-register":
            self.app.push_screen(RegisterModal(self._register_client))
        elif event.button.id == "btn-exit":
            self.app.exit()

    def action_submit(self) -> None:
        self._try_login()
    
    def action_quit(self) -> None:
        self.app.exit()

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

        auth_user = self._authenticate(user, pwd)
        if auth_user is not None:
            app = cast(Any, self.app)
            app.current_user = auth_user["username"]
            app.current_user_id = auth_user.get("id")
            app.current_user_role = auth_user.get("role", "client")
            self._record_event(
                "login_success",
                user_id=auth_user.get("id"),
                username=auth_user["username"],
                user_role=auth_user.get("role", "client"),
            )
            self._on_login_success()
        else:
            err.update("✗  ACCESO DENEGADO — CREDENCIALES INVÁLIDAS")
            self.query_one("#input-pass", Input).value = ""
            self._record_event("login_failed", username=user)

    def _authenticate(self, username: str, password: str) -> dict | None:
        # Delegate authentication to the UserStore (single source of truth)
        if self._user_store is not None:
            return self._user_store.authenticate(username, password)
        return None

    def _register_client(self, username: str, password: str) -> tuple[bool, str]:
        if self._user_store is None:
            return False, "REGISTRO NO DISPONIBLE"
        success, message, user = self._user_store.register_client(username, password)
        if success and user is not None:
            self._record_event(
                "user_registered",
                user_id=user["id"],
                username=user["username"],
                user_role=user["role"],
            )
        else:
            self._record_event(
                "user_registration_failed", username=username, message=message
            )
        return success, message

    def _record_event(self, event_type: str, **details: Any) -> None:
        app = cast(Any, self.app)
        trace = getattr(app, "trace", None)
        if trace is not None:
            trace.record_event(event_type, **details)


class RegisterModal(ModalScreen[None]):
    """Modal para enrolar un usuario cliente."""

    def __init__(
        self, register_callback: Callable[[str, str], tuple[bool, str]], **kwargs
    ):
        super().__init__(**kwargs)
        self._register_callback = register_callback

    def compose(self) -> ComposeResult:
        with Container(id="register-box"):
            yield Static("◈  CREAR CUENTA CLIENTE  ◈", id="register-title")
            yield Label("▸ USUARIO", classes="field-label")
            yield Input(placeholder="nuevo_usuario", id="register-user")
            yield Label("▸ CONTRASEÑA", classes="field-label")
            yield Input(
                placeholder="mínimo 4 caracteres", password=True, id="register-pass"
            )
            yield Label("▸ CONFIRMAR CONTRASEÑA", classes="field-label")
            yield Input(
                placeholder="repite la contraseña",
                password=True,
                id="register-pass-confirm",
            )
            yield Button("⟫  REGISTRAR  ⟪", id="btn-register-confirm")
            yield Button("CANCELAR", id="btn-register-cancel")
            yield Static("", id="register-error")

    def on_mount(self) -> None:
        self.query_one("#register-user", Input).focus()

    @on(Button.Pressed, "#btn-register-confirm")
    def submit_registration(self) -> None:
        username = self.query_one("#register-user", Input).value.strip()
        password = self.query_one("#register-pass", Input).value
        password_confirm = self.query_one("#register-pass-confirm", Input).value
        message = self.query_one("#register-error", Static)

        if not username or not password or not password_confirm:
            message.update("⚠  COMPLETA TODOS LOS CAMPOS")
            return
        if password != password_confirm:
            message.update("✗  LAS CONTRASEÑAS NO COINCIDEN")
            return

        success, result_message = self._register_callback(username, password)
        if not success:
            message.update(f"✗  {result_message}")
            return

        message.update(f"✓  {result_message}")
        self.dismiss()

    @on(Button.Pressed, "#btn-register-cancel")
    def cancel_registration(self) -> None:
        self.dismiss()
