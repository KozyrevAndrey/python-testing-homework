from typing import TypedDict, final
import pytest
import httpretty
import pytest
from mimesis import Field
from typing import Generator
import json


@final
class FakeResponse(TypedDict):
    id: int


@pytest.fixture
def fake_url() -> str:
    return 'https://fake-site.com'


@pytest.fixture
def mock_api_user_response(fake: Field) -> FakeResponse:
    return FakeResponse(id=fake('numeric.increment'))


@pytest.fixture()
def api_mock(
    mock_api_user_response: FakeResponse,
    fake_url: str,
) -> Generator[FakeResponse, None, None]:
    """Mock external api calls."""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.POST,
            body=json.dumps(mock_api_user_response),
            uri='{0}/users'.format(fake_url),
        )
        yield mock_api_user_response
        assert httpretty.has_request()
