from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    OrderViewSet,
    OrderItemViewSet,
<<<<<<< HEAD
    UserViewSet,
    productoViewSet,
=======
    productoViewSet,
    CategoriaViewSet,
    UserViewSet,
>>>>>>> 96d788061ed4e7ab180356a3c646fa36f8d60a5b
)
from .views import (
    productoCreateView,
    ProductoListView

)   

router = DefaultRouter()
router.register(r'Order', OrderViewSet, basename='order')
router.register(r'OrdeItem', OrderItemViewSet, basename='orderitem')
router.register(r'producto', productoViewSet, basename='producto')
router.register(r'categoria', CategoriaViewSet, basename='categoria')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,
]