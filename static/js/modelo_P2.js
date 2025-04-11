document.addEventListener("DOMContentLoaded", () => {
    const input1 = document.getElementById("Peleador_A");
    const input2 = document.getElementById("Peleador_B");
    const img1 = document.getElementById("img1");
    const img2 = document.getElementById("img2");

    img2.style.transform = "scaleX(-1)"; // Voltear la imagen del segundo peleador

    const defaultImg = "/static/img/peleador_default.png";

    let imagenesData = [];

    // Cargar el JSON de imágenes una vez al inicio
    fetch("/data/imagenes.json")
        .then(res => res.json())
        .then(data => {
            imagenesData = data;
        })
        .catch(error => {
            console.error("Error al cargar imagenes.json:", error);
        });

    function obtenerImagen(nombre) {
        const nombreNormalizado = nombre.trim().toLowerCase();
        const peleador = imagenesData.find(p => p.Nombre.trim().toLowerCase() === nombreNormalizado);

        if (peleador && peleador.Imagen && peleador.Imagen !== "NaN") {
            return peleador.Imagen;
        } else {
            return defaultImg;
        }
    }

    function actualizarImagen(input, img) {
        const imagenURL = obtenerImagen(input.value);
        img.src = imagenURL;
    }

    // Mostrar las imágenes predeterminadas al cargar la página
    actualizarImagen(input1, img1);
    actualizarImagen(input2, img2);

    input1.addEventListener("input", () => actualizarImagen(input1, img1));
    input2.addEventListener("input", () => actualizarImagen(input2, img2));

    // Manejo del formulario de predicción
    const form = document.getElementById("formulario-p2");
    const resultadoDiv = document.getElementById("resultado");

    // Antes de usar el gráfico, asegúrate de borrar el anterior si existe
    let chartInstance = null;

    console.log("esto es una prueba")

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const Peleador_A = input1.value;
        const Peleador_B = input2.value;

        console.log("esto es una prueba")

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
            const probability = data.probability;
            const probabilityPercent = (probability * 100).toFixed(2);

            const loser = data.winner === Peleador_A ? Peleador_B : Peleador_A;
            const loserProb = (100 - probabilityPercent).toFixed(2);


            resultadoDiv.innerHTML = `
                <div class="prediction-result">
                    <h3>Resultado de la Predicción</h3>
                    <p><strong>Ganador:</strong> ${data.winner}</p>
                    <p><strong>Probabilidad:</strong> ${probabilityPercent}%</p>
                    <canvas id="pieChart" width="300" height="300"></canvas>
                </div>
            `;

            const ctx = document.getElementById('pieChart').getContext('2d');

            // Determinar el orden de los datos según quién sea el ganador
            const peleadorA_prob = data.winner === Peleador_A ? probabilityPercent : (100 - probabilityPercent).toFixed(2);
            const peleadorB_prob = (100 - peleadorA_prob).toFixed(2);


            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: [Peleador_A, Peleador_B],
                    datasets: [{
                        data: [peleadorA_prob, peleadorB_prob],
                        backgroundColor: ['#d20a0a', '#0a40d2'], // Rojo para A, Azul para B
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#fff',
                                font: {
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                }
            });

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
