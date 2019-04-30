import pytest
from src.app import create_app, db as _db
from src.config import TestConfig


# Default app fixture for testing with TestConfig
@pytest.fixture
def app():
    _app = create_app(conf=TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


if __name__ == "__main__":
    pytest.main(['--tb=short'])
