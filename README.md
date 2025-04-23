# Servidor web para UFC Predictor: Sistema de predicción para la UFC

## Proyecto de Datos I

### Estructura del repositorio

- La carpeta data contiene:
  * `imagenes.json`, archivo que contiene las URL de las fotografías de los peleadores, estas se mostraran en la pagina web.
  * `peleas.parquet`, un dataset en formato Parquet que funciona como la base de datos del proyecto.

- La carpeta models alberga dos modelos XGBoost entrenados:
  * modelP1.xgb – modelo optimizado para generar predicciones post‑combate.
  * modelP2.xgb – modelo optimizado para generar predicciones pre‑combate.
  
- La carpeta static contiene todos los activos que el navegador recibe “tal cual”, sin procesamiento del servidor:
  * `style.css` – hoja de estilos que fija la tipografía, la paleta de color y la maquetación responsive de la interfaz.
  * `js/` – subdirectorio con dos scripts JavaScript:
    * `modelo_p1.js` – lógica de la página de predicción pre‑combate.
    * `modelo_p2.js` – lógica de la página de predicción post‑combate.
  * `img/` – colección de imágenes, iconos y logotipos empleados por la aplicación.

- La carpeta templates agrupa las plantillas HTML que el motor de renderizado sirve dinámicamente. Su organización refleja la composición visual de la aplicación:
 * `base.html`, esqueleto común que define la estructura principal (doctype, <head>, bloques de contenido, carga de scripts/estilos). El resto de páginas extienden esta plantilla.
 * `header.html` y `footer.html`, fragmentos parciales incluidos por base.html para mantener un encabezado y pie de página coherentes en todo el sitio.
 * `navbar.html`, componente de navegación reutilizable con los enlaces a las distintas secciones.
 * `inicio.html`, página de bienvenida que presenta la aplicación y redirige a las áreas de predicción.
 * `modelo_P1.html`, vista dedicada a las predicciones pre‑combate (carga el script modelo_p1.js).
 * `modelo_P2.html` vista análoga para las predicciones post‑combate (carga el script modelo_p2.js).

- El archivo `main.py` contiene la configuración y la implementación principal de la API, utilizando FastAPI como framework para gestionar las rutas y la lógica del servidor.

- El archivo `PasarAP2Difdf.py`,se encarga de procesar las estadísticas de los peleadores para calcular las diferencias entre los valores de dos peleadores A y B.

- El archivo `CalculaFilaP2Dif.py`, se encarga de calcular las estadísticas ponderadas de las últimas tres peleas previas de dos peleadores dados, y genera una fila con las diferencias entre ellos.
 
### Instrucciones para iniciar el entorno de desarrollo con sus dependencias

### Instrucciones para ejecutar ejecutar y probar el servidor web

### Instrucciones para crear la imagen docker y ejecutar el contenedor

### Integrantes 
 -  Andrés Fernández Ortega
 -  Francisco José Pastor Ruiz
 -  Mario Granados Guerrero
 -  Telmo Aracama Docampo
 -  Carlos Vallejo Ros
 -  Mateo Turati Domínguez
