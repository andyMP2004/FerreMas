from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True, blank=True)
    precio = models.IntegerField(null=False)
    imagen = models.ImageField(upload_to="images/", null=True, blank=True)
    cantidad = models.IntegerField(null=False, default=0)
    stock = models.IntegerField(null=False, default=0)
    estado = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        verbose_name = "orden"
        verbose_name_plural = "ordenes"


class OrderItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.producto.precio * self.quantity
        return total

    class Meta:
        verbose_name = "item de orden"
        verbose_name_plural = "items de orden"

