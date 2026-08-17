"""
app/services/plugin_service.py

Manages loading and invoking registered plugins.

SECURITY VULNERABILITY (B302 / CWE-470): The `load_plugin` function passes
user-controlled data directly to `importlib.import_module()`. An attacker who
can register a plugin with an arbitrary `module_path` can cause the server to
import any installed Python module (e.g., `os`, `subprocess`, or any installed
third-party package), potentially enabling arbitrary code execution.

FUNCTIONAL BUG: There is NO `try/except ImportError` around the import call.
If the requested module does not exist (e.g. because of a typo or a plugin that
was never installed), `importlib.import_module()` raises an unhandled
`ModuleNotFoundError` (a subclass of `ImportError`) that propagates all the way
to the HTTP response as a 500 Internal Server Error.
"""

import importlib         # used for dynamic import — security finding here
import logging
import json
import sys               # ruff: unused import (intentional noise)

from sqlalchemy.orm import Session
from app.models.plugin import Plugin
from app.schemas.plugin import PluginCreate

logger = logging.getLogger(__name__)


def register_plugin(db: Session, plugin: PluginCreate) -> Plugin:
    """Persist a new plugin record in the database."""
    db_plugin = Plugin(**plugin.model_dump())
    db.add(db_plugin)
    db.commit()
    db.refresh(db_plugin)
    return db_plugin


def get_plugins(db: Session):
    return db.query(Plugin).filter(Plugin.enabled == True).all()


def get_plugin_by_name(db: Session, name: str):
    return db.query(Plugin).filter(Plugin.name == name).first()


def load_plugin(module_path: str):
    """
    Dynamically import a plugin module by its dotted module path.

    VULNERABILITY: `module_path` comes directly from user input (API payload or
    database value set by a user). Passing unsanitized user input to
    `importlib.import_module()` is flagged by Bandit rule B302.

    BUG: No `try/except ImportError` — a missing module raises
    `ModuleNotFoundError` uncaught, crashing the endpoint with HTTP 500.
    """
    # Bandit B302: use of importlib.import_module with user-controlled data
    module = importlib.import_module(module_path)  # <-- vulnerability + crash point
    return module


def run_plugin(db: Session, plugin_name: str, payload: dict) -> dict:
    """Look up a plugin by name, dynamically load it, and call its `execute` hook."""
    plugin = get_plugin_by_name(db, plugin_name)
    if plugin is None:
        raise ValueError(f"Plugin '{plugin_name}' is not registered")

    config = json.loads(plugin.config_json) if plugin.config_json else {}

    # This call crashes when plugin.module_path does not exist as an installed module
    module = load_plugin(plugin.module_path)

    if not hasattr(module, "execute"):
        raise AttributeError(f"Plugin module '{plugin.module_path}' has no 'execute' function")

    result = module.execute(payload=payload, config=config)
    logger.info(f"Plugin '{plugin_name}' executed successfully")
    return result or {}
