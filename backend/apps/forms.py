from django import forms
from .models import MovimientoInventario, Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "descripcion",
            "precio",
            "imagen",
            "stock",
            
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

class MovimientoInventarioForm(forms.ModelForm):    
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'tipo', 'cantidad', 'observacion']

