FROM python:3.12-slim

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Ensure poetry installs globally in the container
ENV POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies and MS SQL Server drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    ca-certificates \
    build-essential \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
    && apt-get install -y unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add mssql-tools to PATH
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files and install
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
