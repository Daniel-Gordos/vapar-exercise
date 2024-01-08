# VAPAR API Exercise

## Usage

### Prerequisites

* Ensure Python 3.12 is install
* Ensure Poetry (>=1.6) is installed

### Setup

```bash
# Create a virtualenv
poetry env use python

# Install all dependencies
poetry install
```

### Run server locally

```bash
# Ensure a '.env.dev' file is in the root of the repo.
# You can copy the example in .env.dev.example
poetry run uvicorn vapar_exercise.app:app   
# The Swagger docs can then be accessed at 'http://127.0.0.1:8000'
```

### Run tests

```bash
# Ensure a '.env.test' file is in the root of the repo.
# You can copy the example in .env.dev.example
poetry run pytest
```

### Run linter

```bash
poetry run ruff check .
```

### Run formatter

```bash
poetry run ruff format .
```
