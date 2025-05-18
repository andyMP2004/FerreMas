from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    Producto,
    Categoria,
)

# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Order)
admin.site.register(OrderItem)

