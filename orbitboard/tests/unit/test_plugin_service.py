"""
tests/unit/test_plugin_service.py

Tests for dynamic plugin loading.
Two passing tests for the normal (happy-path) flow.
One FAILING test for the unhandled ImportError / ModuleNotFoundError bug.
"""
import pytest

from app.services import plugin_service


# ── Helpers / fixtures ─────────────────────────────────────────────────────────

class _FakePlugin:
    """Simulate a registered plugin DB object."""
    def __init__(self, name, module_path, config_json=None):
        self.name = name
        self.module_path = module_path
        self.config_json = config_json
        self.enabled = True


# ── Passing tests ──────────────────────────────────────────────────────────────

def test_load_builtin_module():
    """
    PASSES — loading a real, installed module (json) must succeed.
    Verifies that load_plugin works when the module path is valid.
    """
    module = plugin_service.load_plugin("json")
    import json as _json
    assert module is _json


def test_load_stdlib_os_module():
    """
    PASSES — loading another real stdlib module (os) must succeed.
    Also demonstrates the SECURITY vulnerability: user-controlled input
    reaches importlib, allowing arbitrary module loading.
    """
    module = plugin_service.load_plugin("os")
    import os as _os
    assert module is _os


# ── Failing test ───────────────────────────────────────────────────────────────

def test_load_nonexistent_plugin_raises_graceful_error():
    """
    FAILS on HEAD with an unhandled ModuleNotFoundError.

    Calling load_plugin() with a module path that is not installed should raise
    a friendly ValueError or HTTPException (404/422), NOT an unhandled
    ModuleNotFoundError.

    Root cause: plugin_service.load_plugin() calls importlib.import_module()
    with no try/except ImportError guard. When the module path does not resolve
    to an installed package, Python raises ModuleNotFoundError which propagates
    uncaught through the service into the FastAPI route handler, producing an
    HTTP 500 instead of an informative error response.

    The pipeline must add:
        try:
            module = importlib.import_module(module_path)
        except ImportError as exc:
            raise ValueError(f"Plugin module not found: {module_path}") from exc
    """
    # This line crashes with unhandled ModuleNotFoundError — it must NOT do so
    plugin_service.load_plugin("orbitboard.plugins.slack_v2_nonexistent")
