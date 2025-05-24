from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_customer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        customer = Customer.objects.create(
            user=request.user,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
        )
        return JsonResponse({"id": customer.id, "name": customer.name}, status=201)

@csrf_exempt
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    if request.method == "PUT":
        data = json.loads(request.body)
        customer.name = data.get("name", customer.name)
        customer.email = data.get("email", customer.email)
        customer.phone = data.get("phone", customer.phone)
        customer.address = data.get("address", customer.address)
        customer.save()
        return JsonResponse({"id": customer.id, "name": customer.name}, status=200)

@csrf_exempt
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    if request.method == "DELETE":
        customer.delete()
        return JsonResponse({"message": "Customer deleted"}, status=204)