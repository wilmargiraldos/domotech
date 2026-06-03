"""Utility package for domo_tech.

Expose commonly used helper functions for other modules in the project.
"""

# Local
from .project_meta import _read_project_meta

read_project_meta = _read_project_meta

__all__ = ["read_project_meta"]
