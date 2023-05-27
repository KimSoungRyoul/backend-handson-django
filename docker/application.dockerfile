FROM python:3.11.1-slim-buster as builder

COPY .  /django-backend-starter
COPY pyproject.toml poetry.lock /django-backend-starter/

# poetry ENV
ENV POETRY_VERSION=1.4.0 \
   POETRY_VIRTUALENVS_CREATE=false \
   PATH="$PATH:/root/.poetry/bin" \
   DEBIAN_FRONTEND=noninteractive \
   DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt-get update && apt-get -y install \
    curl gcc default-libmysqlclient-dev \
    libpq-dev \
    gcc g++ build-essential python3-pandas make cmake python3-pip libgdal20 \
    python3-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev cargo libsodium-dev -y \
    # Cleaning cache:
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir

WORKDIR /django-backend-starter
RUN poetry install --no-interaction --no-ansi --no-dev



FROM python:3.10.1-slim-buster

RUN apt-get update && apt-get -y install nginx default-mysql-client curl \
    # Cleaning cache:
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /django-backend-starter /django-backend-starter

WORKDIR /django-backend-starter
# EXPOSE 8080
ENTRYPOINT ["daphne", "cofig.asgi.application"]
