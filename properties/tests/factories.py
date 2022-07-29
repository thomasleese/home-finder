from django.contrib.gis.geos import Point
import factory

from ..models import Property


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Property

    class Params:
        for_sale = factory.Trait(price_sale=1_000_000)
        for_rent = factory.Trait(price_rent_per_week=250, price_rent_per_month=1_000)

    zoopla_id = factory.Sequence(lambda n: n)

    address = "123 Street, Town, POST CODE"
    location = Point(0, 0)

    url = "https://property/id"

    photos = ["https://property/id/photo"]
    number_of_bedrooms = 2
