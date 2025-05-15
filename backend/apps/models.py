from django.db import models
from django.contrib.auth.models import User


class Libro(models.Model):
    tituloLibro = models.CharField(max_length=200, null=True, blank=True)
    autorLibro = models.CharField(max_length=200, null=True, blank=True)
    anioLibro = models.IntegerField(null=True, blank=True)
    descripcionLibro = models.TextField(max_length=1000, null=True, blank=True)
    precioLibro = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=True, null=True, blank=True)
    portadaLibro = models.ImageField(upload_to="images/", null=True, blank=True)
    archivoLibro = models.FileField(upload_to="documents/", null=True, blank=True)

    def __str__(self):
        return self.tituloLibro

    class Meta:
        verbose_name = "libro"
        verbose_name_plural = "libros"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.libro.digital == False:
                shipping = True
        return shipping

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
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.libro.precioLibro * self.quantity
        return total

    class Meta:
        verbose_name = "item de orden"
        verbose_name_plural = "items de orden"

class TarjetaCompra(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    numeroTarjeta = models.IntegerField(null=False)
    nombreTitular = models.CharField(max_length=200, null=False)
    fechaCaducidad = models.CharField(max_length=200, null=False)
    codigoCvc = models.IntegerField(null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.numeroTarjeta)

    class Meta:
        verbose_name = "tarjeta de compra"
        verbose_name_plural = "tarjetas de compra"




#Adaptacion a Ferremas
# Categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"


# Productos disponibles en FERREMAS
#Este modelo muestra los productos de ferremas
class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True, blank=True)
    precio = models.IntegerField(null=False)
    imagen = models.ImageField(upload_to="images/", null=True, blank=True)
  

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"


"""
#Este modelo muestra los pedidos del usuario
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        return True  # Todos los productos requieren envío

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


# Detalles de cada producto en una orden
class OrderItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.producto.precio * self.quantity

    class Meta:
        verbose_name = "ítem de orden"
        verbose_name_plural = "ítems de orden"


# Datos de tarjeta asociados a una compra
class TarjetaCompra(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    numeroTarjeta = models.BigIntegerField(null=False)
    nombreTitular = models.CharField(max_length=200, null=False)
    fechaCaducidad = models.CharField(max_length=200, null=False)
    codigoCvc = models.IntegerField(null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.numeroTarjeta)

    class Meta:
        verbose_name = "tarjeta de compra"
        verbose_name_plural = "tarjetas de compra" """