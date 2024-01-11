FROM python:3.10-slim

EXPOSE 8000
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Upgrade pip and install Poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN pip install fastapi uvicorn

# Check Poetry version (for debugging purposes)
RUN poetry --version

# Configure Poetry
RUN poetry config virtualenvs.in-project true

# Install dependencies using Poetry
# Verbose output for troubleshooting
COPY pyproject.toml ./
RUN poetry install --no-dev -vvv

# Copy the rest of your application
COPY . ./

# Command to run the application
CMD poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000
