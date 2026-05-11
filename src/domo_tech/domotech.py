"""
DOMO - TECH — Tienda virtual de componentes electrónicos
Modo TUI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instalar:  pip install textual
Ejecutar:  python domotech.py

Usuarios de prueba:
  admin / 1234
  cyber / punk
  user  / pass
"""

from typing import cast

from textual.app import App
from domo_tech.cyber_store import PRODUCTS
from domo_tech.ui.screens.login import LoginScreen, DEFAULT_USERS
from domo_tech.ui.screens.store_screen import Product, StoreScreen
from domo_tech.ui.styles import CYBER_STORE_CSS

# ─── CSS ──────────────────────────────────────────────────────────

CSS = CYBER_STORE_CSS
USE_WIDE_LOGIN_BANNER = False


# ─── App ──────────────────────────────────────────────────────────

class DomoTechStore(App[None]):
    CSS = CSS
    TITLE = "DOMO-TECH"

    current_user: str = ""

    def _show_store(self) -> None:
        self.push_screen(StoreScreen(cast(list[Product], PRODUCTS)))

    def on_mount(self) -> None:
        self.push_screen(
            LoginScreen(
                on_login_success=self._show_store,
                users=DEFAULT_USERS,
                use_wide_banner=USE_WIDE_LOGIN_BANNER,
            )
        )


def main():
    DomoTechStore().run()

if __name__ == "__main__":
    main()