"""Shared pytest fixtures. Fixtures used by more than one test module go here."""

import pytest


@pytest.fixture
def make_user():
    """Factory fixture: build a valid user and override only what the test cares about."""

    def _make(**overrides):
        user = {"email": "qa.user@example.com", "password": "Str0ngPass1", "role": "tester"}
        user.update(overrides)
        return user

    return _make
