document.addEventListener("DOMContentLoaded", () => {
    // Variables de los peleadores y sus imágenes
    const input1 = document.getElementById("Peleador_A");
    const input2 = document.getElementById("Peleador_B");
    const img1 = document.getElementById("img1");
    const img2 = document.getElementById("img2");

    const basePath = "/static/images/fighters/";
    const defaultImg = "https://www.ufc.com/themes/custom/ufc/assets/img/no-profile-image.png";

    // Función para actualizar la imagen
    function actualizarImagen(input, img) {
        const nombre = input.value.trim().toLowerCase().replace(/\s+/g, "_");
        const path = `${basePath}${nombre}.jpg`;

        fetch(path)
            .then(res => {
                img.src = res.ok ? path : defaultImg;
            })
            .catch(() => {
                img.src = defaultImg;
            });
    }

    input1.addEventListener("input", () => actualizarImagen(input1, img1));
    input2.addEventListener("input", () => actualizarImagen(input2, img2));

    // Manejo del formulario de predicción
    const form = document.getElementById("formulario-p2");
    const resultadoDiv = document.getElementById("resultado");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const Peleador_A = input1.value;
        const Peleador_B = input2.value;

        try {
            const response = await fetch("/predictP2_json", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `Peleador_A=${encodeURIComponent(Peleador_A)}&Peleador_B=${encodeURIComponent(Peleador_B)}`
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            const data = await response.json();

            // Formatear la probabilidad como porcentaje con 2 decimales
            const probabilityPercent = (data.probability * 100).toFixed(2);
            
            resultadoDiv.innerHTML = `
                <div class="prediction-result">
                    <h3>Resultado de la Predicción</h3>
                    <p><strong>Ganador:</strong> ${data.winner}</p>
                    <p><strong>Probabilidad:</strong> ${probabilityPercent}%</p>
                </div>
            `;
        } catch (error) {
            console.error("Error en la predicción:", error);
            resultadoDiv.innerHTML = `
                <div class="error-message">
                    <p>Hubo un error en la predicción. Por favor, inténtalo de nuevo.</p>
                </div>
            `;
        }
    });
});