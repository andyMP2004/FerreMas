document.addEventListener("DOMContentLoaded", function () {
  const monedaSelect = document.getElementById("moneda-select");
  const totalElement = document.getElementById("total-amount");
  const totalCLP = parseFloat(totalElement.dataset.clp);

  monedaSelect.addEventListener("change", function () {
    const moneda = this.value;

    if (moneda === "CLP") {
      totalElement.textContent = "$" + totalCLP.toLocaleString("es-CL");
    } else if (moneda === "USD") {
      fetch("/tasa-dolar/")
        .then((response) => response.json())
        .then((data) => {
          if (data.tasa) {
            const tasa = data.tasa;
            const totalUSD = totalCLP / tasa;
            totalElement.textContent = "US$" + totalUSD.toFixed(2);
          } else {
            totalElement.textContent = "Error al obtener tasa";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          totalElement.textContent = "Error de conexión";
        });
    }
  });
});