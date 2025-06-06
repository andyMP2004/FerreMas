from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView,
)

from .models import *
from .forms import ProductoForm

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm})
    else:

        if request.POST["registerPassword"] == request.POST["confirmPassword"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["registerName"],
                    email=request.POST["registerEmail"],
                    password=request.POST["registerPassword"],
                )
                user.save()
                login(request, user)
                return redirect("home_page")

            except IntegrityError:
                return render(
                    request,
                    "register_error.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


def register_error(request):
    return render(request, "register_error.html")


def signin_user(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "signin.html", {"form": form})
    elif request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
            else:
                error = "Username or password is incorrect."
        else:
            error = "Invalid form data. Please check your input."

        return render(request, "signin.html", {"form": form, "error": error})


@login_required
def administracion(request):
    return render(request, "admin/adminhome.html")


class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "admin/productos_list.html"
    context_object_name = "productos"

class HerramientaDetailView( DetailView):
    model = Producto
    template_name = "catalogue_detail.html"
    context_object_name = "Lista"


class ProductosListView(ListView):
    model = Producto
    template_name = "catalogue.html"
    context_object_name = "productos"


class productoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "admin/productos_form.html"
    def form_valid(self, form):
        form.save()
        return redirect("productos_list")
    



class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = [
        "nombre",
        "categoria",
        "descripcion",
        "precio",
        "imagen",
        "stock",

    ]
    template_name = "admin/productos_update.html"
    success_url = reverse_lazy("productos_list")


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "admin/productos_confirm_delete.html"
    success_url = reverse_lazy("productos_list")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "admin/user_list.html"
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ["username", "email", "password", "is_superuser"]
    template_name = "admin/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "admin/user_update.html"
    success_url = reverse_lazy("user_list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "admin/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home_page")


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order

@login_required
def remove_from_cart(request, item_id):
    try:
        # Obtener el item del carrito solo si pertenece al usuario actual y su orden no está completa
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__complete=False)
        order_item.delete()
    except OrderItem.DoesNotExist:
        pass  # Opcional: puedes manejar el error o ignorarlo

    return redirect('cart')  # Asegúrate de que esta URL exista en tus urls.py
def home_page(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "home-page.html", context)

def catalogue_detail(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'catalogue_detail.html', {'producto': producto})

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}

    context = {"items": items, "order": order}
    return render(request, "cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}

    context = {"items": items, "order": order}
    return render(request, "checkout.html", context)

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productoId = data.get("productoId")
    action = data.get("action")

    print("Action:", action)
    print("ProductoId:", productoId)

    user = request.user
    producto = Producto.objects.get(id=productoId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, producto=producto)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    elif action == "delete":
        orderItem.quantity = orderItem.quantity == 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)





#---------------tranbank-------------------
import uuid
from django.http import HttpResponseBadRequest
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

options = WebpayOptions(
    commerce_code='597055555532',
    api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
    integration_type=IntegrationType.TEST
)

tx = Transaction(options)

def iniciar_pago(request):
    if request.method == 'POST':
        amount = int(request.POST.get('total'))
        buy_order = str(uuid.uuid4())[:26]
        session_id = str(uuid.uuid4())[:61]
        return_url = request.build_absolute_uri('/pago/respuesta/')

        response = tx.create(buy_order, session_id, amount, return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")

    return render(request, 'checkout.html')

@csrf_exempt
def respuesta(request):
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token:
        messages.error(request, "Token no recibido.")
        return redirect('checkout')

    response = tx.commit(token)

    if response['status'] == 'AUTHORIZED':
        # Buscar la orden incompleta más reciente del usuario
        order = Order.objects.filter(user=request.user, complete=False).order_by('-date_ordered').first()

        if not order:
            return render(request, 'pago_error.html', {'response': response, 'error': 'No se encontró una orden válida.'})

        order.complete = True
        order.transaction_id = response['buy_order']
        order.date_ordered = timezone.now()
        order.save()

        # Actualizar el stock de los productos
        for item in order.orderitem_set.all():
            producto = item.producto
            producto.stock -= item.quantity
            producto.save()

        return render(request, 'pago_exito.html', {'response': response})

    else:
        return render(request, 'pago_error.html', {'response': response})
    #---------------------------------------------------------------------------
# ! Configuracion Email

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = "Recuperación Contraseña"
        email_content = f"Email: {email}\nSolicita recuperación de contraseña."

        send_mail(
            subject, email_content, email, ["bast.bascunan@duocuc.cl"], fail_silently=False
        )

        return HttpResponseRedirect("/contact/enviado/")

    return render(request, "contact.html")


def contact_enviado(request):
    return render(request, "contact_enviado.html")


# -------------------------------------------------------------------------------
#Cambio de moneda
import requests
from django.http import JsonResponse

from django.http import JsonResponse
import requests

def obtener_tasa_dolar(request):
    try:
        response = requests.get("https://mindicador.cl/api/dolar", timeout=5)
        response.raise_for_status()
        data = response.json()
        serie = data.get("serie", [])
        if serie and isinstance(serie, list):
            tasa = serie[0].get("valor")
            if tasa:
                return JsonResponse({'tasa': tasa})
        return JsonResponse({'error': 'No se pudo obtener la tasa del dólar'}, status=500)
    except requests.RequestException:
        return JsonResponse({'error': 'Error al conectar con el servicio del Banco Central'}, status=500)

#--------------------------------------------------------------------------------

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import  Order, OrderItem
from django.contrib.auth.models import User
from .serializers import (

    CategoriaSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ProductoSerializer,
    UserSerializer,
   
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

<<<<<<< HEAD
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

=======
>>>>>>> 96d788061ed4e7ab180356a3c646fa36f8d60a5b
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class productoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
<<<<<<< HEAD

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
=======
>>>>>>> 96d788061ed4e7ab180356a3c646fa36f8d60a5b

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

from .models import Producto, MovimientoInventario
from .forms import MovimientoInventarioForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_bodeguero(request):
    productos = Producto.objects.all()
    return render(request, 'bodega/bodeguero_dashboard.html', {'productos': productos})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()

            # Actualizar stock
            producto = movimiento.producto
            if movimiento.tipo == 'entrada':
                producto.stock += movimiento.cantidad
            else:
                producto.stock -= movimiento.cantidad
            producto.save()

            return redirect('vista_bodeguero')
    else:
        form = MovimientoInventarioForm()
    return render(request, 'bodega/registrar_movimiento.html', {'form': form})

@login_required
def historial_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related('producto').order_by('-fecha')
    return render(request, 'bodega/historial_movimientos.html', {'movimientos': movimientos})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order, OrderItem
import uuid

@login_required
def checkout_success(request):
    order = Order.objects.filter(user=request.user, complete=False).first()

    if not order:
        return redirect('cart')  # No hay orden pendiente

    # Simulamos obtener los datos del sistema de pago externo
    transaction_id = str(uuid.uuid4())  # O el ID que te da Transbank
    order.transaction_id = transaction_id
    order.complete = True
    order.date_ordered = timezone.now()
    order.save()

    # Puedes cambiar el estado de cada item si es necesario
    for item in order.orderitem_set.all():
        item.estado = 'pendiente'  # o 'confirmado', si prefieres
        item.save()

    return render(request, 'payment_success.html', {
        'response': {
            'buy_order': transaction_id,
            'amount': order.get_cart_total
        }
    })
# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import OrderItem  # o el nombre real de tu modelo
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # solo si tienes problemas de CSRF (no recomendado en producción sin control)
def cambiar_estado_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)
        nuevo_estado = request.POST.get('nuevo_estado')
        if nuevo_estado in ['pendiente', 'entregado']:
            item.estado = nuevo_estado
            item.save()
    return redirect('ordenes')  # Asegúrate que esta URL exista



@login_required
def ver_ordenes_bodega(request):
    # Solo mostramos órdenes completas, con al menos un item pendiente
    ordenes = Order.objects.filter(complete=True, orderitem__estado='pendiente').distinct()

    return render(request, 'Bodega/orden_bodeguero.html', {
        'ordenes': ordenes
    })

