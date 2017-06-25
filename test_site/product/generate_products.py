import random
from elizabeth import Personal, Address, Business, Datetime, Text
from django.contrib.auth.models import User
from .models import Products, Consumers
import datetime


def true_or_false():
    return random.choice([True, False])


def random_price():
    return random.uniform(1.0, 5000.0)


def product_add_to_db(request):
    person_data = Personal('ru')
    person_address = Address('ru')
    busines = Business('ru')
    date = Datetime('ru')
    text = Text('ru')

    for _ in range(301):
        Products.objects.create(
            product_name=text.title(),
            product_slug=person_data.cid(),
            product_description=text.text(quantity=5),
            product_price=random_price(),
            product_created_at=date.date(start=2017, end=2017, fmt='%Y-%m-%d %H:%M:%S'),
            product_modified_at=date.date(start=2017, end=2017, fmt='%Y-%m-%d %H:%M:%S'),
        )
    for _ in range(127):

        user = User.objects.create(
            username='test{}'.format(str(datetime.datetime.now().microsecond)),
            password='qwerty1234'
        )
        Consumers.objects.create(
            user=user,
            full_name=person_data.full_name(),
            banned=true_or_false(),
            gender=person_data.gender(),
        )


if __name__ == '__main__':
    product_add_to_db()