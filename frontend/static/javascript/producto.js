document.addEventListener('DOMContentLoaded', function() {
    var ProductoForm = document.getElementById('ProductoForm');

    if (ProductoForm) {
        ProductoForm.addEventListener('submit', function(event) {
            event.preventDefault(); 

            var productoNombreInput = document.getElementById('productoName');
            var productoCategoriaInput = document.getElementById('categoria');
            var descripcionInput = document.getElementById('descripcion');
            var precioInput = document.getElementById('precio');
            var imagenInput = document.getElementById('imagen');

            if (productoNombreInput && productoCategoriaInput && descripcionInput && precioInput && imagenInput) {
                if (productoNombreInput.value && productoCategoriaInput.value && descripcionInput.value && precioInput.value && imagenInput.value) {
                    ProductoForm.submit();
                } else {
                    var feedback = document.getElementById('feedback');
                    if (feedback) {
                        feedback.textContent = 'Por favor completa todos los campos.';
                        feedback.classList.add('text-danger');
                    }
                }
            }
        });
        }
});