#!/usr/bin/env python3
"""
Demo script to display all available Domo-Tech logos and ASCII art.

Usage:
    poetry run python -m domo_tech.ui.logo_demo
"""

from domo_tech.ui.branding import (
    LOGO_MINIMALIST,
    LOGO_DOMO_TECH_COMPACT,
    LOGO_DOMO_TECH_FULL,
    LOGO_CYBERPUNK_CIRCUIT,
    LOGO_DOMOTECH,
    HEADER_STORE,
    SPLASH_WELCOME,
    BANNER_COMPONENTS,
    BANNER_TECH_STACK,
    BANNER_PROMO,
    CATEGORY_ARDUINO,
    CATEGORY_RASPBERRY,
    CATEGORY_SENSORS,
    CATEGORY_ACTUATORS,
    CATEGORY_CONNECTIVITY,
)


def display_menu():
    """Display interactive logo selector."""
    logos = {
        "1": ("LOGO_MINIMALIST", LOGO_MINIMALIST),
        "2": ("LOGO_DOMO_TECH_COMPACT", LOGO_DOMO_TECH_COMPACT),
        "3": ("LOGO_DOMO_TECH_FULL", LOGO_DOMO_TECH_FULL),
        "4": ("LOGO_CYBERPUNK_CIRCUIT", LOGO_CYBERPUNK_CIRCUIT),
        "5": ("LOGO_DOMOTECH", LOGO_DOMOTECH),
        "6": ("HEADER_STORE", HEADER_STORE),
        "7": ("SPLASH_WELCOME", SPLASH_WELCOME),
        "8": ("BANNER_COMPONENTS", BANNER_COMPONENTS),
        "9": ("BANNER_TECH_STACK", BANNER_TECH_STACK),
        "10": ("BANNER_PROMO", BANNER_PROMO),
        "11": ("CATEGORY_ARDUINO", CATEGORY_ARDUINO),
        "12": ("CATEGORY_RASPBERRY", CATEGORY_RASPBERRY),
        "13": ("CATEGORY_SENSORS", CATEGORY_SENSORS),
        "14": ("CATEGORY_ACTUATORS", CATEGORY_ACTUATORS),
        "15": ("CATEGORY_CONNECTIVITY", CATEGORY_CONNECTIVITY),
        "all": ("ALL", None),
    }

    print("\n" + "=" * 70)
    print("DOMO-TECH: ASCII ART LOGOS & BANNERS GALLERY")
    print("=" * 70)
    print("\nAvailable logos:\n")

    for key, (name, _) in logos.items():
        print(f"  {key:>2}. {name}")

    print("\nEnter a number to view a logo, or 'all' to display all.")
    print("Press Ctrl+C to exit.\n")

    return logos


def main():
    """Main demo function."""
    logos = display_menu()

    while True:
        try:
            choice = input("Select logo [1-15 or 'all']: ").strip().lower()

            if choice in logos:
                name, logo = logos[choice]

                if choice == "all":
                    # Display all logos
                    for key, (n, l) in logos.items():
                        if key != "all":
                            print("\n" + "=" * 70)
                            print(f"[{key}] {n}")
                            print("=" * 70)
                            print(l)
                            input("\nPress Enter to continue...")
                else:
                    print("\n" + "=" * 70)
                    print(f"[{choice}] {name}")
                    print("=" * 70)
                    print(logo)
                    input("\nPress Enter to continue...")

            elif choice == "q":
                print("\n✌️  Goodbye!\n")
                break

            elif choice == "code":
                # Show copy-paste Python code
                print("\n" + "=" * 70)
                print("COPY-PASTE CODE EXAMPLES")
                print("=" * 70)
                print_code_examples()
                input("\nPress Enter to continue...")

            else:
                print("❌ Invalid choice. Try again.\n")

        except KeyboardInterrupt:
            print("\n\n✌️  Goodbye!\n")
            break
        except EOFError:
            print("\n\n✌️  Goodbye!\n")
            break


def print_code_examples():
    """Print code examples for integrating logos."""
    examples = """
# Example 1: Using logos in your Textual app
from domo_tech.ui import HEADER_STORE, LOGO_MINIMALIST
from textual.widgets import Static

class BrandingHeader(Static):
    def render(self):
        return HEADER_STORE

class WelcomeSplash(Static):
    def render(self):
        return LOGO_MINIMALIST


# Example 2: Displaying in your cyber_store.py LoginScreen
from domo_tech.ui import SPLASH_WELCOME

class LoginScreen(Screen):
    def on_mount(self):
        # Display logo in login screen
        self.query_one("#logo", Static).update(SPLASH_WELCOME)


# Example 3: Creating a gallery screen
from domo_tech.ui.branding import (
    LOGO_MINIMALIST, LOGO_DOMO_TECH_COMPACT,
    CATEGORY_ARDUINO, CATEGORY_SENSORS
)

class GalleryScreen(Screen):
    def compose(self):
        yield Static(LOGO_MINIMALIST, id="logo")
        yield Static(CATEGORY_ARDUINO, id="category_1")
        yield Static(CATEGORY_SENSORS, id="category_2")


# Example 4: Store Header in StoreScreen
from domo_tech.ui import HEADER_STORE

class StoreScreen(Screen):
    def compose(self):
        yield Static(HEADER_STORE, id="header")
        yield Static("Your store content here", id="content")


# Example 5: Showing in terminal/CLI
from domo_tech.ui import SPLASH_WELCOME, BANNER_COMPONENTS

print(SPLASH_WELCOME)
print(BANNER_COMPONENTS)
"""
    print(examples)


if __name__ == "__main__":
    main()
