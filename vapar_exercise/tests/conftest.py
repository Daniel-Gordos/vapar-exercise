from pathlib import Path
from httpx import AsyncClient, MockTransport, Request, Response
import pytest
from vapar_exercise.app import app
from vapar_exercise.config import Config
from vapar_exercise.dependencies import get_config

_example_github_response = Path(
    "vapar_exercise/tests/github_api_example_response.json"
).read_text()


@pytest.fixture
def test_app_client():
    test_client = AsyncClient(app=app, base_url="http://testserver")

    config = Config(_env_file=".env.test")  # type:ignore - Loaded from env file
    app.dependency_overrides = {
        get_config: lambda: config,
    }

    yield test_client


@pytest.fixture
def mock_http_client():
    def handler(req: Request) -> Response:
        return Response(200, text=_example_github_response)

    transport = MockTransport(handler)
    client = AsyncClient(transport=transport)
    yield client


@pytest.fixture
def mock_http_client_no_user():
    def handler(req: Request) -> Response:
        return Response(404)

    transport = MockTransport(handler)
    client = AsyncClient(transport=transport)
    yield client
