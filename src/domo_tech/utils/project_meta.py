"""Utilities for reading project metadata (name/version).

This is used by UI screens and other code that wants a consistent
project name+version regardless of whether the package is installed
or being run from source.
"""

from __future__ import annotations

# Standard library
from importlib import metadata as _metadata
from pathlib import Path
import tomllib
from typing import Tuple


def _read_project_meta() -> Tuple[str, str]:
    """Return (name, version) for the project.

    Strategy:
    1. Try `importlib.metadata` for an installed distribution (checks
       common names).
    2. Fallback to reading nearest `pyproject.toml` upwards from this file.
    3. Final fallback to sensible defaults.
    """
    # 1) Try importlib.metadata (works when package is installed)
    try:
        for dist_name in ("domo-tech", "domo_tech", "domo_tech"):
            try:
                ver = _metadata.version(dist_name)
                try:
                    meta = _metadata.metadata(dist_name)
                    name = meta.get("Name") or dist_name
                except Exception:
                    name = dist_name
                return name, ver
            except _metadata.PackageNotFoundError:
                continue
    except Exception:
        # ignore metadata errors and fallback to file lookup
        pass

    # 2) Search for pyproject.toml in parent dirs
    try:
        p = Path(__file__).resolve()
        for parent in p.parents:
            candidate = parent / "pyproject.toml"
            if candidate.exists():
                with candidate.open("rb") as f:
                    data = tomllib.load(f)
                proj = data.get("project", {}) or {}
                name = str(proj.get("name") or "DOMO-TECH")
                version = str(proj.get("version") or "0.0.0")
                return name, version
    except Exception:
        pass

    # 3) final fallback
    return "DOMO-TECH", "0.0.0"
