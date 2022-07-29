from django.db import IntegrityError
import pytest


@pytest.mark.django_db
class TestUser:
    def test_unique_username(self, user, user_factory):
        with pytest.raises(IntegrityError, match="duplicate"):
            user_factory(username=user.username)
