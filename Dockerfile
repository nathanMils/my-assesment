FROM python:3.10

WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy only the pyproject.toml and optionally poetry.lock to cache the dependency installation layer
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry in the system python environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev -vvv

# I wanted to use volumes instead
# # Copy the rest of your application
# COPY . /app # Uncomment if you want to use compose
COPY . /app

# Expose the port Jupyter will run on
EXPOSE 8888

# Start Jupyter notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
