Project Structure
-----------------

The project follows a modular, industry-standard structure for Python TUI applications:

```
src/domo_tech/
├── __init__.py
├── db/                         # Persistence layer (SQLite + SQLAlchemy)
│   ├── __init__.py
│   ├── base.py                 # Declarative ORM base
│   ├── models.py               # User, Product, Order, OrderItem models
│   ├── session.py              # Engine and SessionLocal factory
│   ├── repositories.py         # UserRepository, ProductRepository, OrderRepository
│   ├── seed_db.py              # Database initialization and seeding
│   └── reports.py              # Export utilities (CSV, JSON)
├── ui/                         # UI components and styling
│   ├── __init__.py
│   ├── cyber_store.py          # Main TUI application (Textual app)
│   └── styles/                 # CSS stylesheets for UI
│       ├── __init__.py
│       └── cyber_store.py      # Cyber Store CSS definitions
└── ...
```

**Key Structure Decisions:**
- **`db/` package**: Centralized persistence layer, separating business logic from UI.
- **`ui/styles/` package**: CSS extracted from components into dedicated stylesheets, following DRY principles.
- **`ui/branding.py`**: ASCII art logos, banners, and brand assets for terminal display.
- **`repositories.py`**: Data access layer with clean CRUD and business logic methods.
- **`reports.py`**: Utilities for exporting and analyzing data (CSV, JSON, CLI).

Branding & Logos
----------------

The project includes a comprehensive ASCII art branding system for **Domo-Tech** — a cyberpunk-themed store specializing in smart home electronics (Arduino, Raspberry Pi, sensors, actuators).

**View all available logos:**

```bash
poetry run python -m domo_tech.ui.logo_demo
```

This interactive demo displays 15+ logos, banners, and category headers that you can use throughout the TUI application.

**Using logos in your code:**

```python
from domo_tech.ui import (
    HEADER_STORE,
    LOGO_MINIMALIST,
    SPLASH_WELCOME,
    BANNER_COMPONENTS,
)

# Display in Textual widgets
class MyScreen(Screen):
    def compose(self):
        yield Static(HEADER_STORE, id="header")
        yield Static(SPLASH_WELCOME, id="splash")
```

**Available logos** (`src/domo_tech/ui/branding.py`):
- `LOGO_MINIMALIST` — Compact header-friendly logo
- `LOGO_DOMO_TECH_COMPACT` — Branded compact version
- `LOGO_DOMO_TECH_FULL` — Full ASCII art logo
- `LOGO_CYBERPUNK_CIRCUIT` — Cyberpunk-themed variant
- `HEADER_STORE` — Main store header with branding
- `SPLASH_WELCOME` — Large welcome screen ASCII art
- `BANNER_COMPONENTS` — Component categories banner
- `CATEGORY_ARDUINO`, `CATEGORY_RASPBERRY`, etc. — Product category headers

**Integration Guide:**

See [src/domo_tech/ui/integration_guide.py](src/domo_tech/ui/integration_guide.py) for detailed examples of how to integrate logos into:
- LoginScreen with welcome splash
- StoreScreen with branded headers
- New dedicated screens (WelcomeScreen, CategoriesScreen)
- CSS styling for logo containers

Run the guide:
```bash
poetry run python -m domo_tech.ui.integration_guide
```

**Customize your own logos:**

Edit `src/domo_tech/ui/branding.py` to:
- Modify existing ASCII art designs
- Add new logos for your brand
- Create seasonal/promotional banners
- Generate product-specific headers

Project setup & persistence
---------------------------

1. Install dependencies (using Poetry):

```bash
poetry install
```

2. (Re)create and populate the SQLite database used by the project:

```bash
# Create the database file and seed example data
poetry run python -m domo_tech.db.seed_db
```

The database file is created at `data/app.db` by default. To change the location, set the environment variable `DOMO_TECH_DB` before running the seed script, for example:

```bash
set DOMO_TECH_DB=data/my_app.db      # Windows PowerShell/CMD
export DOMO_TECH_DB=data/my_app.db   # Unix-like shells
poetry run python -m domo_tech.db.seed_db
```

3. Quick example of using the persistence layer from Python:

```python
from domo_tech.db.session import SessionLocal
from domo_tech.db.repositories import UserRepository, ProductRepository

with SessionLocal() as session:
	ur = UserRepository(session)
	pr = ProductRepository(session)

	user = ur.authenticate("admin", "1234")
	products = pr.list_products()
	print(user, products)
```

If you need migrations instead of `create_all`, initialize Alembic and generate migrations (optional for this academic project).

Reportes y exportación
----------------------

Ejemplos rápidos para consultar históricos y exportar reportes desde la capa de persistencia.

- Obtener histórico de compras de un usuario y volcar a CSV:

```python
from domo_tech.db.session import SessionLocal
from domo_tech.db.repositories import OrderRepository
import csv

user_id = 1  # id del usuario

with SessionLocal() as session:
	orr = OrderRepository(session)
	orders = orr.get_user_orders(user_id)

	# Exportar a CSV
	with open('user_orders.csv', 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(['order_id', 'created_at', 'status', 'total'])
		for o in orders:
			writer.writerow([o.id, o.created_at.isoformat(), o.status, o.total])

```

- Obtener histórico de ventas (admin) y volcar a JSON con detalles de items:

```python
from domo_tech.db.session import SessionLocal
from domo_tech.db.repositories import OrderRepository
import json

with SessionLocal() as session:
	orr = OrderRepository(session)
	orders = orr.get_all_orders()

	out = []
	for o in orders:
		items = []
		for it in o.items:
			items.append({
				'product_id': it.product_id,
				'qty': it.qty,
				'unit_price': it.unit_price,
			})
		out.append({
			'order_id': o.id,
			'user_id': o.user_id,
			'created_at': o.created_at.isoformat(),
			'status': o.status,
			'total': o.total,
			'items': items,
		})

	with open('sales_report.json', 'w', encoding='utf-8') as f:
		json.dump(out, f, indent=2, ensure_ascii=False)

```

Estos ejemplos usan la capa de repositorios ya incluida en `src/domo_tech/db/repositories.py`. Puedes adaptar los filtros (por fecha, por producto, por categoría) añadiendo métodos en `OrderRepository`.

Usar el script de reportes
-------------------------

También hay un script/CLI pequeño en `src/domo_tech/db/reports.py` que facilita exportar:

```bash
# Exportar órdenes de un usuario a CSV
poetry run python -m domo_tech.db.reports --user-csv 1 user_orders.csv

# Exportar todas las órdenes a JSON
poetry run python -m domo_tech.db.reports --all-json sales_report.json
```

Estos comandos usan la misma configuración de `data/app.db` y las `SessionLocal`/repositorios.

