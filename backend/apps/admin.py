from django.contrib import admin
from .models import (
    Libro,
    Order,
    OrderItem,
    TarjetaCompra,
    Producto,
    Categoria,
)

# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(TarjetaCompra)
