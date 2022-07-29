from django.db import IntegrityError
import pytest


@pytest.mark.django_db
class TestProperty:
    @pytest.mark.parametrize(
        "price_sale,price_rent_per_week,price_rent_per_month",
        [
            (None, None, None),
            (100, 1, 4),
            (100, 1, None),
            (100, None, 4),
        ],
    )
    def test_property_price_constraint(
        self, property_factory, price_sale, price_rent_per_week, price_rent_per_month
    ):
        with pytest.raises(IntegrityError):
            property_factory(
                price_sale=price_sale,
                price_rent_per_week=price_rent_per_week,
                price_rent_per_month=price_rent_per_month,
            )
