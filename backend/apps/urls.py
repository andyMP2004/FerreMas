from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    OrderItemViewSet,
    productoViewSet,
    CategoriaViewSet,
    UserViewSet,
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