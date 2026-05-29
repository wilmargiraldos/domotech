# Guía de Desarrollo - Domo-Tech

Esta guía proporciona las instrucciones necesarias para compilar y ejecutar la aplicación **domo-tech** en tu entorno local, partiendo del supuesto de que tienes únicamente Python base instalado.

## Requisitos Previos

- **Python 3.14 o superior** (menor que 4.0)
- Una terminal o símbolo del sistema (PowerShell, cmd, bash, etc.)
- Acceso a internet para descargar las dependencias

## Paso 1: Verificar la Instalación de Python

Abre una terminal y verifica que Python está instalado correctamente:

```bash
python --version
# O también puedes usar:
python3 --version
```

Debes ver una versión igual o superior a **3.14.0**.

## Paso 2: Instalar Poetry

Poetry es el gestor de dependencias que utiliza este proyecto. Existen varias formas de instalarlo:

### Opción A: Instalar Poetry usando pip (Recomendado)

```bash
python -m pip install --upgrade pip
python -m pip install poetry
```

### Opción B: Instalar Poetry usando el script oficial

Si prefieres usar el instalador oficial de Poetry, ejecuta:

```bash
# En Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# En macOS/Linux:
curl -sSL https://install.python-poetry.org | python3 -
```

Después de instalar con el script oficial, asegúrate de que Poetry esté en tu variable PATH. Para verificar:

```bash
poetry --version
```

Si el comando no se reconoce, consulta la documentación oficial de Poetry: https://python-poetry.org/docs/#installation

### Verificar la Instalación de Poetry

```bash
poetry --version
# Debes ver algo como: Poetry (version 1.x.x)
```

## Paso 3: Clonar o Descargar el Proyecto

Si aún no has descargado el proyecto, clónalo o descárgalo en tu máquina:

```bash
# Si usas Git:
git clone <URL_DEL_REPOSITORIO> domo-tech
cd domo-tech

# O simplemente navega a la carpeta del proyecto:
cd domo-tech
```

## Paso 4: Instalar las Dependencias del Proyecto

Una vez dentro de la carpeta del proyecto, instala todas las dependencias necesarias usando Poetry:

```bash
poetry install
```

Este comando hará lo siguiente:
- Leerá el archivo `pyproject.toml`
- Descargará todas las dependencias especificadas
- Creará un entorno virtual aislado para el proyecto
- Generará o actualizará el archivo `poetry.lock` con las versiones exactas instaladas

**Nota**: La primera instalación puede tomar algunos minutos.

### Dependencias Principales

El proyecto requiere las siguientes bibliotecas (instaladas automáticamente por Poetry):

- **rich** (>=15.0.0): Para formateo avanzado de texto en la terminal
- **pyfiglet** (>=1.0.4): Para crear arte ASCII/figlet
- **textual** (>=8.2.5): Framework para interfaces de usuario en terminal
- **sqlalchemy** (>=2.0.49): ORM para manejo de bases de datos
- **bcrypt** (>=4.0.0): Para hash seguro de contraseñas
- **alembic** (>=1.11.0): Para migraciones de base de datos

## Paso 5: Verificar la Instalación

Verifica que el entorno está configurado correctamente:

```bash
# Activa el entorno virtual de Poetry
poetry shell

# O ejecuta comandos dentro del entorno con:
poetry run python --version
```

## Paso 6: Ejecutar la Aplicación

Hay varias formas de ejecutar la aplicación, dependiendo de lo que quieras hacer:

### Opción A: Ejecutar el Entry Point Principal (Recomendado)

El entry point principal es `domotech`. Puedes ejecutarlo directamente:

```bash
# Si estás dentro del shell de Poetry:
poetry shell
domotech

# O sin activar el shell:
poetry run domotech
```

### Opción B: Ejecutar directamente el archivo Python

Si prefieres ejecutar el archivo directamente sin usar el entry point:

```bash
poetry run python src/domo_tech/domotech.py
```

### Opción C: Ejecutar otros Entry Points

El proyecto incluye varios entry points. Aquí están todos disponibles:

```bash
# Cyber Store
poetry run cyber-store

# Terminal Nexus
poetry run terminal-nexus

# Prueba
poetry run prueba

# Logo Demo
poetry run domotech-logo

# Integration Guide
poetry run domotech-guide
```

## Paso 7: Trabajar en el Proyecto (Desarrollo)

Si necesitas realizar cambios en el código:

### Editar el Código

1. Abre el proyecto en tu editor favorito (VS Code, PyCharm, etc.)
2. Los archivos fuente están en `src/domo_tech/`
3. Modifica los archivos según sea necesario

### Ejecutar la Aplicación con Cambios

Después de hacer cambios, ejecuta la aplicación de nuevo. Poetry se asegurará de que siempre se use el código más reciente:

```bash
poetry run domotech
```

### Instalar Nuevas Dependencias

Si necesitas agregar nuevas dependencias al proyecto:

```bash
# Para dependencias de producción:
poetry add nombre_del_paquete

# Para dependencias de desarrollo:
poetry add --group dev nombre_del_paquete
```

Poetry actualizará automáticamente `pyproject.toml` y `poetry.lock`.

## Paso 8: Desactivar el Entorno Virtual

Cuando termines de trabajar:

```bash
# Si estás dentro del shell de Poetry:
exit

# O simplemente cierra la terminal
```

## Usuarios cargados por defecto:

- admin / 1234
- cyber / punk
- user  / pass

## Estructura del Proyecto

```
domo-tech/
├── src/domo_tech/          # Código fuente principal
│   ├── domotech.py         # Entry point principal
│   ├── cyber_store.py      # Módulo de tienda
│   ├── db/                 # Base de datos
│   ├── ui/                 # Interfaz de usuario
│   └── ...
├── tests/                  # Pruebas unitarias
├── data/                   # Datos de prueba
├── pyproject.toml          # Configuración del proyecto
└── poetry.lock             # Versiones exactas de dependencias
```

## Persistencia de Datos

Actualmente la persistencia permanente del proyecto se basa en archivos JSON ubicados en la carpeta `data/`. Esta carpeta contiene los archivos que la aplicación utiliza para guardar y recuperar información entre ejecuciones, por lo que su contenido representa el estado persistente actual del sistema.

Estos archivos se crean automáticamente cuando no existen, ya sea porque nunca fueron generados o porque fueron eliminados de forma intencional. En ese caso, la aplicación reconstruye la persistencia mínima necesaria para seguir funcionando.

Aunque en `pyproject.toml` se han declarado dependencias relacionadas con SQL y migraciones, esa capa de persistencia todavía no está implementada en la aplicación. Por ese motivo, no debe asumirse que la base de datos relacional forme parte del comportamiento final ni que sustituya a los archivos JSON existentes.

En la práctica, esto significa lo siguiente:

- Los datos que la aplicación necesita conservar de una ejecución a otra se leen y escriben en los archivos de `data/`.
- Si se modifica o elimina alguno de esos archivos, la aplicación volverá a crearlos con una carga inicial de prueba al iniciar.
- Los archivos JSON funcionan como la fuente de verdad actual mientras no se complete una implementación alternativa de persistencia.
- Cualquier cambio futuro hacia una base de datos deberá hacerse de forma explícita y no debe darse por hecho solo por la presencia de dependencias SQL en el proyecto.

Los archivos de esta carpeta deben tratarse como parte importante del entorno de ejecución, aunque su contenido inicial corresponda a datos de prueba usados para la carga inicial de la aplicación.


## Solución de Problemas

### Problema: "Poetry no se reconoce como comando"

**Solución**: 
- Asegúrate de que Poetry está en la variable PATH de tu sistema
- Reinicia la terminal después de instalar Poetry
- Usa la ruta completa al ejecutable de Poetry si es necesario

### Problema: "Versión de Python no compatible"

**Solución**:
- El proyecto requiere Python 3.14 o superior
- Verifica tu versión con `python --version`
- Si necesitas una versión específica, considera usar pyenv o asdf

### Problema: Error al instalar dependencias con Poetry

**Solución**:
- Asegúrate de estar en la carpeta correcta del proyecto
- Intenta actualizar Poetry: `pip install --upgrade poetry`
- Limpia la caché de Poetry: `poetry cache clear . --all`
- Intenta de nuevo: `poetry install`

### Problema: Cambios en el código no se reflejan

**Solución**:
- Poetry ejecuta el código en el entorno virtual
- Los cambios se reflejan automáticamente la próxima vez que ejecutes el comando
- Si aún así no funciona, desactiva y reactiva el entorno virtual

## Recursos Adicionales

- [Documentación Oficial de Poetry](https://python-poetry.org/docs/)
- [Documentación de Python 3.14](https://docs.python.org/3.14/)
- [Textual Documentation](https://textual.textualize.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Notas Importantes

- El archivo `poetry.lock` debe ser incluido en el control de versiones para garantizar reproducibilidad
- Nunca modifiques manualmente `poetry.lock`
- Siempre usa `poetry install` para instalar dependencias en nuevos entornos
- Para reproducibilidad exacta, usa `poetry install --no-root` si solo necesitas las dependencias

## Contacto y Soporte

Si tienes problemas específicos con el proyecto, consulta el archivo `README.md` o contacta al mantenedor del proyecto.
