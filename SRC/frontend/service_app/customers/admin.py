from django.contrib import admin

# Register your models here.
# add the customer model to the admin
from .models import Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at',)
    search_fields = ('name', 'email')
    list_filter = ('is_deleted',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_deleted=False)  # Only show non-deleted customers