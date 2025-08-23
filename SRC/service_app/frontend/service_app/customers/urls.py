from django.urls import path
from . import views

urlpatterns = [
    path("customers/create/", views.create_customer, name="create_customer"),
    path("customers/<int:customer_id>/update/", views.update_customer, name="update_customer"),
    path("customers/<int:customer_id>/delete/", views.delete_customer, name="delete_customer"),
]