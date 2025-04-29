// Función que muestra el resultado de la predicción en el HTML
function mostrarResultado(resultado) {
    const ganador=resultado.winner
    const probabilidad=(resultado.probability*100).toFixed(2)
    const contenedor = document.getElementById('resultado'); // Obtiene el contenedor donde se mostrará el resultado
    contenedor.innerHTML = `
            <h3>Resultado de la Predicción</h3>
            <p><strong>Ganador:</strong> ${ganador}</p>
            <p><strong>Probabilidad:</strong> ${probabilidad}%</p>
            </div>`
    contenedor.style.display = 'block'; // Asegura que el contenedor sea visible
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formulario-p1").addEventListener("submit", async function(event){
        event.preventDefault(); // Evita recarga de la página
        const formData = new FormData(this); // Crea un objeto FormData con los datos del formulario

        // Envía una petición POST al servidor con los datos del formulario
        const response = await fetch("/PrediccionPostCombate", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor'); // Lanza un error si la respuesta no fue exitosa
        }
        const resultado = await response.json(); 
        mostrarResultado(resultado);
    });
});
