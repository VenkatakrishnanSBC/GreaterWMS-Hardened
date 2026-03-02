"""
GreaterWMS Test Configuration

This conftest.py provides shared fixtures and configuration for all tests.
"""
import os
import pytest
import django
from django.conf import settings


# Ensure Django is configured before anything else runs
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greaterwms.settings')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    This is needed because GreaterWMS uses database-backed models extensively.
    """
    pass


@pytest.fixture
def api_client():
    """Provide a DRF APIClient instance."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user():
    """Factory fixture for creating test users."""
    from userprofile.models import Users

    def _create_user(openid=None, appid=None, name="Test User"):
        import uuid
        openid = openid or str(uuid.uuid4())
        appid = appid or str(uuid.uuid4())
        user = Users.objects.create(
            openid=openid,
            appid=appid,
            name=name,
            user_id=Users.objects.count() + 1,
        )
        return user

    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Provide an authenticated APIClient with a test user."""
    user = create_user()
    api_client.credentials(HTTP_TOKEN=user.openid)
    return api_client, user
