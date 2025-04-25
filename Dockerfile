# Base image
FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8000"]

# Una vez construida la imagen con el comando
# $ docker build -t webapp .
# Se podrá ejecutar un contenedor con el comando
# $ docker run -p 8000:8000 webapp
# Y probar la app en la URL
# http://localhost:8000/static/flower.html

