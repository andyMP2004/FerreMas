from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    OrderItemViewSet,
)
from .views import (
    productoCreateView,
    ProductoListView

)   

router = DefaultRouter()
router.register(r'Order', OrderViewSet, basename='order')
router.register(r'OrdeItem', OrderItemViewSet, basename='orderitem')


urlpatterns = [
    *router.urls,
]