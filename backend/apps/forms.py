from django import forms
from .models import Libro
from .models import Producto

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            "tituloLibro",
            "autorLibro",
            "anioLibro",
            "descripcionLibro",
            "precioLibro",
            "digital",
            "portadaLibro",
            "archivoLibro",
        ]
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "descripcion",
            "precio",
            "imagen",
            
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
