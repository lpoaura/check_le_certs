FROM python:3.12-slim AS base
LABEL maintainer="@lpofredc"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

FROM base AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

COPY . .
RUN poetry install
RUN poetry build

FROM base AS final

RUN groupadd -r -g 1000 appuser && useradd --no-log-init -r -g 1000 -d /home/appuser -m -u 1000 appuser && \
    chown -R appuser /home/appuser

COPY --from=builder /app/dist/*.whl /tmp/

RUN pip install /tmp/*.whl

USER appuser

ENTRYPOINT ["check_certs"]