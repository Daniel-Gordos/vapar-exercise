from httpx import AsyncClient, MockTransport
import pytest
from vapar_exercise.app import app
from vapar_exercise.config import Config
from vapar_exercise.dependencies import get_config


@pytest.fixture
def test_app_client():
    test_client = AsyncClient(app=app, base_url="http://testserver")

    config = Config(_env_file=".env.test")  # type:ignore - Loaded from env file
    app.dependency_overrides = {
        get_config: lambda: config,
    }

    yield test_client


@pytest.fixture
def mock_http_client_factory():
    def factory(handler):
        transport = MockTransport(handler)
        return AsyncClient(transport=transport)

    yield factory
