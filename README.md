Domo-Tech
=========

Aplicación TUI de tienda virtual para el flujo oficial definido en `src/domo_tech/domotech.py`.

La ejecución real de la app pasa por estas piezas:
- `domotech.py` como punto de entrada principal.
- `users.py`, `inventory.py` y `tracing.py` como capa de estado persistente en JSON dentro de `data/`.
- `ui/screens/login.py`, `ui/screens/store_screen.py`, `ui/screens/admin_screen.py`, `ui/screens/cart_item.py` y `ui/screens/modals.py` como interfaz.
- `ui/branding.py` y `ui/styles/cyber_store.py` como branding y estilos.

Estructura actual
-----------------

```text
data
├── audit_log.jsonl
├── inventory.json
├── sales_history.json
├── users.json
src/domo_tech/
├── __init__.py
├── domotech.py
├── inventory.py
├── tracing.py
├── users.py
├── ui/
│   ├── __init__.py
│   ├── branding.py
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── admin_screen.py
│   │   ├── cart_item.py
│   │   ├── login.py
│   │   ├── modals.py
│   │   └── store_screen.py
│   └── styles/
│       ├── __init__.py
│       └── cyber_store.py
└── utils/
    ├── __init__.py
    └── project_meta.py
```

Lo que quedó fuera del flujo oficial
-----------------------------------

Se movieron a `unused/` los módulos que no participan en la ejecución normal de `domotech.py` y que correspondían a prototipos, guías o capas alternativas de persistencia.

Arranque
--------

El proyecto usa `poetry` y declara `textual` como dependencia. La forma recomendada de ejecutar la app es:

```powershell
poetry install
poetry run domotech
```

También puedes ejecutar el archivo directamente, siempre que el entorno activo ya tenga las dependencias instaladas:

```powershell
python src/domo_tech/domotech.py
```

Datos de ejecución
------------------

La aplicación guarda su estado en archivos JSON bajo `data/`:
- `data/users.json`
- `data/inventory.json`
- `data/sales_history.json`
- `data/audit_log.jsonl`

Si esos archivos no existen, la app los recrea con datos base al arrancar.

Usuarios iniciales
------------------

- `admin / 1234`
- `cyber / punk`
- `user / pass`

Notas

Utilidad `project_meta`
-----------------------

Se extrajo la lógica de detección de nombre y versión del proyecto a una utilidad reutilizable:

- Módulo: `src/domo_tech/utils/project_meta.py`
- Función exportada: `read_project_meta()` → devuelve `(name, version)`

Esto permite que otras partes del código (por ejemplo `ui/screens/login.py`) obtengan metadatos del proyecto de forma consistente tanto si el paquete está instalado como si se ejecuta desde el árbol de fuentes.

Ejemplo de uso:

```python
from domo_tech.utils import read_project_meta
name, version = read_project_meta()
```
- El script `domotech` está registrado en `pyproject.toml` como entry point del proyecto.
- La documentación y los ejemplos de base de datos relacional, reportes CLI y demos gráficos quedaron fuera porque no forman parte del flujo oficial de `domotech.py`.
- La carpeta `unused/` sirve para conservar el historial de piezas retiradas mientras se decide su eliminación definitiva.
