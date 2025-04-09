document.addEventListener("DOMContentLoaded", () => {
    // Variables de los peleadores y sus imágenes
    const input1 = document.getElementById("Peleador_A");
    const input2 = document.getElementById("Peleador_B");
    const img1 = document.getElementById("img1");
    const img2 = document.getElementById("img2");

    const basePath = "/static/images/fighters/";  // Ruta base para las imágenes de los peleadores
    const defaultImg = "https://www.ufc.com/themes/custom/ufc/assets/img/no-profile-image.png";  // Imagen por defecto

    // Función para actualizar la imagen al escribir el nombre del peleador
    function actualizarImagen(input, img) {
        const nombre = input.value.trim().toLowerCase().replace(/\s+/g, "_");
        const path = `${basePath}${nombre}.jpg`;

        fetch(path)
            .then(res => {
                img.src = res.ok ? path : defaultImg;  // Cambiar imagen si existe o usar la imagen por defecto
            })
            .catch(() => {
                img.src = defaultImg;  // Usar la imagen por defecto si no se encuentra la imagen del peleador
            });
    }

    // Actualizar imágenes cuando el usuario escribe en los campos de los peleadores
    input1.addEventListener("input", () => actualizarImagen(input1, img1));
    input2.addEventListener("input", () => actualizarImagen(input2, img2));

    // Manejo del formulario de predicción
    const form = document.getElementById("formulario-p2");
    const resultadoDiv = document.getElementById("resultado");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();  // Evitar que el formulario se envíe de la manera tradicional

        const Peleador_A = document.getElementById("Peleador_A").value;
        const Peleador_B = document.getElementById("Peleador_B").value;

        const formData = new FormData();
        formData.append("Peleador_A", Peleador_A);
        formData.append("Peleador_B", Peleador_B);

        try {
            const response = await fetch("/predictP2_json", {
                method: "POST",
                body: formData,  // Enviar los datos del formulario
            });

            const data = await response.json();  // Obtener la respuesta en formato JSON

            // Mostrar el resultado dinámicamente en el mismo lugar sin recargar la página
            resultadoDiv.innerHTML = `
                <h3>Resultado de la Predicción</h3>
                <p><strong>Ganador:</strong> ${data.winner}</p>
                <p><strong>Probabilidad:</strong> ${data.probability}%</p>
            `;
        } catch (error) {
            console.error("Error en la predicción:", error);
            resultadoDiv.innerHTML = `<p style="color:red">Hubo un error en la predicción.</p>`;  // Mostrar mensaje de error
        }
    });
});
