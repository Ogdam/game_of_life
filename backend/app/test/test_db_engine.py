import db.engine as db_engine_module
from db.engine import create_db_engine, create_session_factory

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"


def test_create_db_engine_delegates_to_sqlalchemy_with_pool_pre_ping(monkeypatch):
    calls = {}

    def _fake_create_async_engine(database_url, **kwargs):
        calls["database_url"] = database_url
        calls["kwargs"] = kwargs
        return "fake-engine"

    monkeypatch.setattr(
        db_engine_module, "create_async_engine", _fake_create_async_engine
    )

    engine = create_db_engine(DATABASE_URL)

    assert engine == "fake-engine"
    assert calls == {"database_url": DATABASE_URL, "kwargs": {"pool_pre_ping": True}}


def test_create_session_factory_delegates_to_sqlalchemy(monkeypatch):
    calls = {}

    def _fake_async_sessionmaker(engine, **kwargs):
        calls["engine"] = engine
        calls["kwargs"] = kwargs
        return "fake-sessionmaker"

    monkeypatch.setattr(
        db_engine_module, "async_sessionmaker", _fake_async_sessionmaker
    )

    factory = create_session_factory("fake-engine")

    assert factory == "fake-sessionmaker"
    assert calls == {"engine": "fake-engine", "kwargs": {"expire_on_commit": False}}
