document.addEventListener("DOMContentLoaded", () => {
    const input1 = document.getElementById("Peleador_A");
    const input2 = document.getElementById("Peleador_B");
    const datalist1 = document.getElementById("peleadoresA");
    const datalist2 = document.getElementById("peleadoresB");
    const img1 = document.getElementById("img1");
    const img2 = document.getElementById("img2");

    // Imagen por defecto en caso de que no se encuentre imagen específica
    const defaultImg = "/static/img/peleador_default.png";

    let imagenesData = [];
    let nombresPeleadores = [];

    // Cargar el archivo JSON con los nombres e imágenes de los peleadores
    fetch("/data/imagenes.json")
        .then(res => res.json())
        .then(data => {
            imagenesData = data;
            nombresPeleadores = data.map(p => p.Nombre); // Extraer solo los nombres
            console.log("Nombres de peleadores cargados:", nombresPeleadores); // Depuración
        })
        .catch(error => {
            console.error("Error al cargar imagenes.json:", error);
        });

    // Buscar y devolver la URL de la imagen correspondiente al nombre del peleador
    function obtenerImagen(nombre) {
        const nombreNormalizado = nombre.trim().toLowerCase();
        const peleador = imagenesData.find(p => p.Nombre.trim().toLowerCase() === nombreNormalizado);

        if (peleador && peleador.Imagen && peleador.Imagen !== "NaN") {
            return peleador.Imagen;
        } else {
            return defaultImg;
        }
    }

    // Actualizar la imagen mostrada según el valor actual del input
    function actualizarImagen(input, img) {
        const imagenURL = obtenerImagen(input.value);
        img.src = imagenURL;
    }

    // Función para actualizar las opciones del datalist
    // Función para actualizar las opciones del datalist
    function actualizarDatalist(input, datalist) {
        const valor = input.value.toLowerCase();
        datalist.innerHTML = ""; // Limpiar opciones previas

        // Filtrar nombres que coincidan parcialmente con el texto ingresado
        const sugerencias = nombresPeleadores
            .filter(nombre => nombre.toLowerCase().includes(valor))
            .slice(0, 8); // Limitar a 8 resultados

        console.log("Sugerencias generadas:", sugerencias); // Depuración

        // Crear opciones para el datalist
        sugerencias.forEach(nombre => {
            const option = document.createElement("option");
            option.value = nombre;
            datalist.appendChild(option);
        });
    }


    // Escuchar eventos de entrada en los campos de texto
    input1.addEventListener("input", () => {
        actualizarDatalist(input1, datalist1);
        actualizarImagen(input1, img1);
    });

    input2.addEventListener("input", () => {
        actualizarDatalist(input2, datalist2);
        actualizarImagen(input2, img2);
    });

    // Mostrar imágenes predeterminadas al cargar la página
    actualizarImagen(input1, img1);
    actualizarImagen(input2, img2);

    // Actualizar imagen en tiempo real al modificar el input
    input1.addEventListener("input", () => actualizarImagen(input1, img1));
    input2.addEventListener("input", () => actualizarImagen(input2, img2));

    // Obtener referencias al formulario y al contenedor de resultados
    const form = document.getElementById("formulario-p2");
    const resultadoDiv = document.getElementById("resultado");

    // Mantener una instancia del gráfico para poder destruirlo antes de crear uno nuevo
    let chartInstance = null;

    console.log("esto es una prueba")

    // Manejar el envío del formulario, hacer fetch al servidor y mostrar predicción
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const Peleador_A = input1.value;
        const Peleador_B = input2.value;

        console.log("esto es una prueba")

        try {
            // Enviar datos de los peleadores al backend y recibir la predicción
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

            // Crear el gráfico circular para mostrar visualmente las probabilidades
            const ctx = document.getElementById('pieChart').getContext('2d');

            // Determinar el orden de los datos según quién sea el ganador
            const peleadorA_prob = data.winner === Peleador_A ? probabilityPercent : (100 - probabilityPercent).toFixed(2);
            const peleadorB_prob = (100 - peleadorA_prob).toFixed(2);


            // Si ya hay un gráfico creado, destruirlo antes de crear uno nuevo
            if (chartInstance) {
                chartInstance.destroy();
            }

            // Crear una nueva instancia del gráfico circular (pie chart)
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

        // Mostrar mensaje de error si la predicción falla
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
