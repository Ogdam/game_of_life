import logging

from logging_config import configure_logging


def _reset_root_handlers(monkeypatch):
    # basicConfig() est un no-op si le root logger a déjà des handlers
    # (ex: import de app.main dans un autre test de la session).
    monkeypatch.setattr(logging.getLogger(), "handlers", [])


def test_configure_logging_sets_level_from_env(monkeypatch):
    _reset_root_handlers(monkeypatch)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    configure_logging()

    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_defaults_to_info(monkeypatch):
    _reset_root_handlers(monkeypatch)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    configure_logging()

    assert logging.getLogger().level == logging.INFO
