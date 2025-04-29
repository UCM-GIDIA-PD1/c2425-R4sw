# Servidor web para UFC Predictor: Sistema de predicción para la UFC
![imageheader](https://github.com/user-attachments/assets/283a70ee-d10a-4658-9e2a-cbfa237b6949)

## Estructura del repositorio

- La carpeta data contiene:
  * `imagenes.json`: Archivo que contiene las URL de las fotografías de los peleadores, estas se mostrarán en la página web.
  * `peleas.parquet`: Dataset en formato Parquet que funciona como la base de datos del proyecto.

- La carpeta models alberga dos modelos XGBoost entrenados:
  * `modelP1.xgb`: Modelo optimizado para generar predicciones post‑combate.
  * `modelP2.xgb`: Modelo optimizado para generar predicciones pre‑combate.
  
- La carpeta static contiene todos los activos que el navegador recibe “tal cual”, sin procesamiento del servidor:
  * `style.css`: Hoja de estilos que fija la tipografía, la paleta de color y la maquetación responsive de la interfaz.
  * `js/`: Subdirectorio con dos scripts JavaScript:
    * `modelo_p1.js`: Lógica de la página de predicción pre‑combate.
    * `modelo_p2.js`: Lógica de la página de predicción post‑combate.
  * `img/`: Carpeta que cuenta con la colección de imágenes, iconos y logotipos empleados por la aplicación.

- La carpeta templates agrupa las plantillas HTML que el motor de renderizado sirve dinámicamente. Su organización refleja la composición visual de la aplicación:
 * `base.html`: Esqueleto común que define la estructura principal (doctype, <head>, bloques de contenido, carga de scripts/estilos). El resto de páginas extienden esta plantilla.
 * `header.html` y `footer.html`: Fragmentos parciales incluidos por base.html para mantener un encabezado y pie de página coherentes en todo el sitio.
 * `navbar.html`: Componente de navegación reutilizable con los enlaces a las distintas secciones.
 * `inicio.html`: Página de bienvenida que presenta la aplicación y redirige a las áreas de predicción.
 * `modelo_P1.html`: Vista dedicada a las predicciones pre‑combate (carga el script modelo_p1.js).
 * `modelo_P2.html`: Vista análoga para las predicciones post‑combate (carga el script modelo_p2.js).

- El archivo `main.py` contiene la configuración y la implementación principal de la API, utilizando FastAPI como framework para gestionar las rutas y la lógica del servidor.

- El archivo `PasarAP2Difdf.py` se encarga de procesar las estadísticas de los peleadores para calcular las diferencias entre los valores de dos peleadores A y B.

- El archivo `CalculaFilaP2Dif.py` se encarga de calcular las estadísticas ponderadas de las últimas tres peleas previas de dos peleadores dados, y genera una fila con las diferencias entre ellos.

- El archivo `Dockerfile` es un archivo de configuración que define cómo se construye la imagen Docker para el proyecto.
  
## Instrucciones para iniciar el entorno de desarrollo con sus dependencias

A continuación se detallan los pasos necesarios para iniciar el proyecto en un entorno de desarrollo local, asegurando que todas las dependencias estén correctamente instaladas.

#### 1. Clona el repositorio:

Primero, clona el repositorio en tu máquina local usando Git:

```
git clone https://github.com/UCM-GIDIA-PD1/c2425-R4sw.git
cd c2425-R4sw
```

#### 2. Instala las dependencias con el siguiente comando:

```
uv sync
```
Esto creará automáticamente un entorno virtual y descargará todas las dependencias especificadas.

#### 3. Activar el entorno virtual 

* En Linux/macOS:
```
source venv/bin/activate
```

* En Windows:
```
.venv/Scripts/activate
```

## Instrucciones para ejecutar ejecutar y probar el servidor web

#### 1. Iniciar la aplicación

Para iniciar el servidor de desarrollo de FastAPI, usa el siguiente comando:
```
uvicorn main:app --reload
```
El parámetro `--reload` permite que el servidor se reinicie automáticamente cada vez que realices cambios en el código.

#### 2. Acceder a la aplicación
   
Una vez que el servidor esté corriendo, puedes acceder a la aplicación desde tu navegador en la siguiente URL:

```
http://127.0.0.1:8000
```

#### 3. Detener el servidor

Para detener el servidor, simplemente presiona `Ctrl+C` en la terminal.

## Instrucciones para crear la imagen docker y ejecutar el contenedor

Esta sección explica cómo empaquetar por completo la aplicación dentro de una imagen Docker y ponerla en marcha en un contenedor, sin necesidad de instalar Python ni dependencias en tu máquina anfitriona.

#### 1. Pre‑requisitos

- Tener Docker Engine instalado y en funcionamiento (versión 20.10 o superior).
- Estar situado en la raíz del repositorio, donde se encuentra el `Dockerfile`.

#### 2. Construir la imagen

Ejecuta el siguiente comando para crear la imagen.

```
docker build -t webapp .
```

Ejecutar el contenedor Docker en una imagen llamada ```webapp```  

```
docker run -p 8000:8000 webapp
```

#### 3. Probar la aplicación

Con el contenedor corriendo, abre el navegador y accede a http://localhost:8000.

#### 4. Detener y eliminar el contenedor

Para parar temporalmente:

```
docker stop <nombre o id del contenedor>
```

Para eliminarlo definitivamente (contenedor detenido):

```
docker rm <nombre o id del contenedor>
```

#### 5. (Optativo) Reconstruir la imagen tras cambios

Si modificas código o dependencias, vuelve a construir la imagen:

```
docker build -t webapp .
```

## Equipo de desarrollo

 -  Andrés Fernández Ortega
 -  Francisco José Pastor Ruiz
 -  Mario Granados Guerrero
 -  Telmo Aracama Docampo
 -  Carlos Vallejo Ros
 -  Mateo Turati Domínguez

Mención especial y agradecimientos a nuestro profesor Antonio Alejandro Sánchez Ruiz-Granados por su constante ayuda y supervisión a lo largo del desarrollo del proyecto.

