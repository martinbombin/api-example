FROM python:3.13-bookworm AS builder

RUN pip install poetry==2.0.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR


FROM python:3.13-slim-bookworm AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb3 \
        libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /code

COPY ./app ./app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]