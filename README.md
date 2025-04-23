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
