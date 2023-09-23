import pytest
from mimesis import Field, Locale


@pytest.fixture
def fake() -> Field:
    """Returns mimesis field as basic element for generating data."""
    return Field(locale=Locale.RU)
