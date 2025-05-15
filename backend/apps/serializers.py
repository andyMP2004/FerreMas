from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Libro,
    Order,
    OrderItem,
    TarjetaCompra,
    Producto,
    Categoria,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class LibroSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Libro
        fields = "__all__"

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


# Serializer para productos
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
class OrderSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = OrderItem
        fields = "__all__"


class TarjetaCompraSerializer(serializers.ModelSerializer):   
    class Meta:
        model = TarjetaCompra
        fields = "__all__"