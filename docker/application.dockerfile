FROM python:3.11.1-slim-buster

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

COPY .  /django-backend-starter

WORKDIR /django-backend-starter
RUN poetry install --without dev,test
RUN poetry run python apps/manage.py collectstatic --no-input

WORKDIR /django-backend-starter/apps
EXPOSE 8000
CMD ["gunicorn", "config.asgi:application", "--workers", "4", "--threads", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind","0.0.0.0:8000"]
# use daphne if you need http2.0
#CMD ["daphne", "-b 0.0.0.0","-p 8000", "cofig.asgi:application"]
