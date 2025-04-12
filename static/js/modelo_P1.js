function mostrarResultado(resultado) {
    const contenedor = document.getElementById('resultado');
    contenedor.innerHTML = `
        <div class="prediction-result">
        <h3>Resultado de la Predicción</h3>
        <p><strong>Ganador:</strong> ${resultado.winner}</p>
        <p><strong>Probabilidad:</strong> ${resultado.probability}%</p>
        </div>`
        contenedor.style.display = 'block';
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formulario-p1").addEventListener("submit", async function(event){
        event.preventDefault(); // Evita recarga de la página
        const formData = new FormData(this);
        const response = await fetch("/PrediccionPostCombate", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        const resultado = await response.json(); 
        mostrarResultado(resultado);
    });
});
