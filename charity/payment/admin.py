from django.contrib import admin
from .models import Order
from unfold.admin import ModelAdmin


@admin.register(Order)
class ClickPaymentAdmin(ModelAdmin):
    list_display = ['id', 'customer_name', 'total_cost', 'payment_method', 'is_paid']
    list_display_links = ['id', 'customer_name']
