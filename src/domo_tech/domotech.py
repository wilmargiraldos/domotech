"""
DOMO - TECH — Tienda virtual de componentes electrónicos
Modo TUI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Third-party
from textual.app import App

# Local
from domo_tech.inventory import InventoryStore
from domo_tech.ui.screens.admin_screen import AdminScreen
from domo_tech.ui.screens.login import LoginScreen
from domo_tech.ui.screens.store_screen import StoreScreen
from domo_tech.ui.styles import CYBER_STORE_CSS
from domo_tech.tracing import TraceStore
from domo_tech.users import UserStore

# ─── CSS ──────────────────────────────────────────────────────────

CSS = CYBER_STORE_CSS
USE_WIDE_LOGIN_BANNER = False

# ─── App ──────────────────────────────────────────────────────────


class DomoTechStore(App[None]):
    CSS = CSS
    TITLE = "DOMO-TECH"

    current_user: str = ""
    current_user_id: int | None = None
    current_user_role: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = InventoryStore()
        self.trace = TraceStore()
        self.users = UserStore()

    def _show_store(self) -> None:
        current_role = str(getattr(self, "current_user_role", "") or "")
        if current_role == "admin":
            self.push_screen(
                AdminScreen(
                    users_store=self.users,
                    inventory_store=self.inventory,
                    trace_store=self.trace,
                )
            )
            return

        self.push_screen(
            StoreScreen(
                self.inventory.list_products(),
                inventory_store=self.inventory,
                trace_store=self.trace,
            )
        )

    def on_mount(self) -> None:
        self.push_screen(
            LoginScreen(
                on_login_success=self._show_store,
                user_store=self.users,
                use_wide_banner=USE_WIDE_LOGIN_BANNER,
            )
        )


def main():
    DomoTechStore().run()


if __name__ == "__main__":
    main()
