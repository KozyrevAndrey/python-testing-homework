import os
from typing import Generator

import pytest
from server.apps.identity.intrastructure.services.placeholder import (
    LeadCreate,
    UserResponse
)
from server.apps.identity.models import User
from server.settings.components.placeholder import PLACEHOLDER_API_URL
#from tests.plugins.mock_url.mock_placeholder import FakeResponse

pytestmark = [pytest.mark.django_db]


def test_create_using_fake_api(
    create_user: User,
    api_mock: Generator['FakeResponse', None, None],
    fake_url: str,
) -> None:
    user = create_user
    response = LeadCreate(fake_url, 5)(user=user)

    assert response == UserResponse(
        **api_mock
    )


@pytest.mark.slow()
@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    'url',
    [
        PLACEHOLDER_API_URL,
        pytest.param(
            'https://fakeapi.com:5200',
            marks=pytest.mark.skipif(
                os.getenv('DJANGO_ENV') == 'production',
                reason='This test is not supposed to be run in production',
            ),
        ),
    ],
)
def test_lead_create_using_real_api(
    create_user: User,
    url: str,
) -> None:
    LeadCreate(url, 10)(user=create_user)
