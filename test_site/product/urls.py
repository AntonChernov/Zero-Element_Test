from django.conf.urls import url, include
from .views import *
from .generate_products import product_add_to_db
urlpatterns = [
    url(r'^product/(?P<id>\d+)/', ViewProductItem.as_view()),
    url(r'^add_products_in_to_base/', product_add_to_db),
    url(r'^is_username/(?P<username>\w+)/', test_username_and_create_new_user),
    url(r'^register/', test_username_and_create_new_user),
    url(r'^reg_str/', register),
    url(r'^all/', ViewListOfProducts.as_view()),
]
