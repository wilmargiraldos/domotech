"""
Integration guide for Domo-Tech ASCII logos with the TUI application.

This module shows multiple ways to integrate the new branding/logos
into the existing cyber_store.py and other screens.
"""

# ============================================================================
# EXAMPLE 1: Update LoginScreen to show logo
# ============================================================================
EXAMPLE_1 = """
from textual.widgets import Static
from domo_tech.ui import SPLASH_WELCOME  # New import

class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        # Add logo before login form
        yield Static(SPLASH_WELCOME, id="login-splash")  # <-- NEW
        
        with Container(id="login-container"):
            yield Static("Usuario:", classes="label")
            yield Input(id="input-user", classes="input-field")
            # ... rest of login form
"""

# ============================================================================
# EXAMPLE 2: Update StoreScreen header with new branding
# ============================================================================
EXAMPLE_2 = """
from domo_tech.ui import HEADER_STORE  # New import
from textual.widgets import Static

class StoreScreen(Screen):
    def compose(self) -> ComposeResult:
        # Replace current header with branded header
        yield Static(HEADER_STORE, id="store-branding")  # <-- NEW
        
        # Then add your existing content
        with Horizontal(id="main-area"):
            # Products panel
            # Cart panel
            # etc...
"""

# ============================================================================
# EXAMPLE 3: Create new Welcome/Splash Screen
# ============================================================================
EXAMPLE_3 = """
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal
from domo_tech.ui import SPLASH_WELCOME, BANNER_COMPONENTS

class WelcomeScreen(Screen):
    '''First screen shown to user with branding and intro.'''
    
    BINDINGS = [("enter", "continue", "Continue")]
    
    def compose(self):
        with Vertical(id="welcome-container"):
            yield Static(SPLASH_WELCOME, id="splash")
            yield Static(BANNER_COMPONENTS, id="banner")
            yield Static("")  # spacer
            
            with Horizontal(id="welcome-buttons"):
                yield Button("INICIAR SESIÓN", id="btn-login", variant="primary")
                yield Button("VER CATÁLOGO", id="btn-catalog")
                yield Button("SALIR", id="btn-exit")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-login":
            self.app.push_screen("login")
        elif event.button.id == "btn-catalog":
            self.app.push_screen("store")
        elif event.button.id == "btn-exit":
            self.app.exit()
"""

# ============================================================================
# EXAMPLE 4: Create Product Categories screen
# ============================================================================
EXAMPLE_4 = """
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import ScrollableContainer, Vertical
from domo_tech.ui.branding import (
    CATEGORY_ARDUINO,
    CATEGORY_RASPBERRY,
    CATEGORY_SENSORS,
    CATEGORY_ACTUATORS,
    CATEGORY_CONNECTIVITY,
)

class CategoriesScreen(Screen):
    '''Display product categories with formatted headers.'''
    
    BINDINGS = [("q", "back", "Back")]
    
    def compose(self):
        with ScrollableContainer(id="categories-scroll"):
            with Vertical(id="categories-list"):
                yield Static(CATEGORY_ARDUINO)
                yield Static(CATEGORY_RASPBERRY)
                yield Static(CATEGORY_SENSORS)
                yield Static(CATEGORY_ACTUATORS)
                yield Static(CATEGORY_CONNECTIVITY)
    
    def action_back(self):
        self.app.pop_screen()
"""

# ============================================================================
# EXAMPLE 5: Add logo to existing cyber_store.py LoginScreen
# ============================================================================
EXAMPLE_5 = """
# Current cyber_store.py imports
from domo_tech.ui.styles import CYBER_STORE_CSS
from domo_tech.ui import LOGO_MINIMALIST  # <-- ADD THIS

class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        # Insert logo at top
        yield Static(LOGO_MINIMALIST, id="login-logo")  # <-- ADD THIS
        
        with Container(id="login-container"):
            yield Static("🔐 DOMO-TECH LOGIN", id="login-title")
            yield Static("", id="login-error")
            
            # ... rest of existing code
"""

# ============================================================================
# EXAMPLE 6: Create a Store Info screen
# ============================================================================
EXAMPLE_6 = """
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal
from domo_tech.ui import HEADER_STORE, BANNER_COMPONENTS, BANNER_TECH_STACK

class StoreInfoScreen(Screen):
    '''Information about Domo-Tech store and tech stack.'''
    
    BINDINGS = [("q", "back", "Back")]
    
    def compose(self):
        with Vertical(id="info-container"):
            yield Static(HEADER_STORE, id="header")
            yield Static("")  # spacer
            yield Static(BANNER_COMPONENTS, id="components")
            yield Static("")  # spacer
            yield Static(BANNER_TECH_STACK, id="tech-stack")
            yield Static("")  # spacer
            
            with Horizontal(id="info-buttons"):
                yield Button("VOLVER", id="btn-back", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.action_back()
    
    def action_back(self):
        self.app.pop_screen()
"""

# ============================================================================
# EXAMPLE 7: CSS styling for logo containers (add to CYBER_STORE_CSS)
# ============================================================================
EXAMPLE_7 = """
# Add these CSS rules to src/domo_tech/ui/styles/cyber_store.py

/* Logo and branding containers */
#login-splash,
#store-branding,
#splash {
    border: solid $accent;
    margin: 1 2;
    padding: 1;
    background: $boost;
    height: auto;
}

#welcome-container {
    width: 100%;
    height: 100%;
    align: center middle;
    padding: 1 2;
}

#welcome-buttons {
    margin-top: 2;
    align: center middle;
    width: 100%;
}

#categories-scroll {
    width: 100%;
    height: 100%;
    padding: 1;
}

.category-header {
    border: heavy $primary;
    margin: 1 0;
    padding: 1;
}
"""

# ============================================================================
# EXAMPLE 8: Run-time usage (terminal/debugging)
# ============================================================================
EXAMPLE_8 = """
# You can display logos from Python directly for testing/debugging:

from domo_tech.ui import (
    LOGO_MINIMALIST,
    HEADER_STORE,
    SPLASH_WELCOME,
    BANNER_COMPONENTS,
)

# Print to terminal for CLI-based usage
print(SPLASH_WELCOME)
print(HEADER_STORE)

# Or in tests/examples
def test_logo_display():
    assert len(LOGO_MINIMALIST) > 0
    assert "DOMO-TECH" in HEADER_STORE
    assert len(SPLASH_WELCOME) > 100
"""

# ============================================================================
# EXAMPLE 9: Updated pyproject.toml scripts with logo demo
# ============================================================================
EXAMPLE_9 = """
# Add to pyproject.toml [project.scripts] section:

[project.scripts]
cyber-store = "domo_tech.cyber_store:main"
terminal-nexus = "domo_tech.terminal_nexus:main"
prueba = "domo_tech.prueba:main"
domotech = "domo_tech.cyber_store:main"
domotech-logo = "domo_tech.ui.logo_demo:main"  # <-- ADD THIS

# Usage: poetry run domotech-logo
"""

# ============================================================================
# EXAMPLE 10: Quick integration checklist
# ============================================================================
INTEGRATION_CHECKLIST = """
╔════════════════════════════════════════════════════════════╗
║           DOMO-TECH LOGO INTEGRATION CHECKLIST            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  DISPLAY LOGOS:                                            ║
║  □ Test with: poetry run python -m domo_tech.ui.logo_demo ║
║  □ Review all available designs                           ║
║  □ Choose preferred logos for your app                    ║
║                                                            ║
║  IMPORT LOGOS:                                             ║
║  □ from domo_tech.ui import HEADER_STORE, LOGO_MINIMALIST ║
║  □ from domo_tech.ui.branding import *                    ║
║                                                            ║
║  INTEGRATE TO TUI:                                         ║
║  □ Add SPLASH_WELCOME to LoginScreen                      ║
║  □ Add HEADER_STORE to StoreScreen                        ║
║  □ Create WelcomeScreen with SPLASH_WELCOME               ║
║  □ Create CategoriesScreen with category logos            ║
║  □ Update CSS for logo containers                         ║
║                                                            ║
║  TEST & VALIDATE:                                          ║
║  □ Run cyber-store and check visual appearance            ║
║  □ Verify logos display correctly in all screens          ║
║  □ Check alignment and spacing                            ║
║  □ Test responsiveness on different terminal sizes        ║
║                                                            ║
║  OPTIONAL ENHANCEMENTS:                                    ║
║  □ Add animation to logos (Textual Animation support)     ║
║  □ Create themed color variants                           ║
║  □ Add seasonal/promotional logos                         ║
║  □ Generate custom logos for specific categories          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# Guide content
# ============================================================================
INTEGRATION_GUIDE = f"""
{'='*70}
DOMO-TECH: LOGO INTEGRATION GUIDE
{'='*70}

PART 1: EXPLORE AVAILABLE LOGOS
────────────────────────────────────────────────────────────────────

Run the demo script to see all available logos:

    poetry run python -m domo_tech.ui.logo_demo

This will show:
- 5 different logo designs
- 10+ banners and headers
- Product category headers
- Promotional banners
- Tech stack information

Choose your favorites for integration!


PART 2: UNDERSTANDING THE STRUCTURE
────────────────────────────────────────────────────────────────────

Location: src/domo_tech/ui/branding.py

All logos are organized in this module:
- LOGO_* constants: Main store logos
- BANNER_* constants: Promotional/info banners
- CATEGORY_* constants: Product category headers
- HEADER_STORE: Main store header
- SPLASH_WELCOME: Full-screen welcome art

Import anywhere in your code:

    from domo_tech.ui import HEADER_STORE, LOGO_MINIMALIST
    from domo_tech.ui.branding import SPLASH_WELCOME


PART 3: BASIC INTEGRATION
────────────────────────────────────────────────────────────────────

{EXAMPLE_1}

{EXAMPLE_5}


PART 4: ADVANCED INTEGRATIONS
────────────────────────────────────────────────────────────────────

Create new screens with branded content:

{EXAMPLE_3}

{EXAMPLE_4}

{EXAMPLE_6}


PART 5: CSS STYLING
────────────────────────────────────────────────────────────────────

Add these styles to make logos look better:

{EXAMPLE_7}


PART 6: QUICK START CHECKLIST
────────────────────────────────────────────────────────────────────

{INTEGRATION_CHECKLIST}


PART 7: PYTHON USAGE EXAMPLES
────────────────────────────────────────────────────────────────────

{EXAMPLE_8}

{EXAMPLE_9}


PART 8: NEXT STEPS
────────────────────────────────────────────────────────────────────

1. Run the demo: poetry run python -m domo_tech.ui.logo_demo
2. Choose your preferred logos
3. Update cyber_store.py to use HEADER_STORE and LOGO_MINIMALIST
4. Create new screens (WelcomeScreen, CategoriesScreen) with logos
5. Update CSS for better visual appearance
6. Test the application: poetry run cyber-store


CUSTOMIZATION IDEAS
────────────────────────────────────────────────────────────────────

- Modify colors/symbols to match your brand
- Create seasonal variations (Navidad, Año Nuevo)
- Add animated ASCII effects for important elements
- Generate product-specific logos
- Create category-specific banners
- Add loading/progress animations


For more information, see:
- src/domo_tech/ui/branding.py
- src/domo_tech/ui/logo_demo.py
- Run: poetry run python -m domo_tech.ui.logo_demo

{'='*70}
"""

if __name__ == "__main__":
    print(INTEGRATION_GUIDE)
