FROM python:3.11.4-slim-bullseye

# poetry ENV
ENV POETRY_VERSION=1.5.0 \
   POETRY_VIRTUALENVS_CREATE=false \
   PATH="$PATH:/root/.poetry/bin" \
   DEBIAN_FRONTEND=noninteractive \
   DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt update && apt -y install gcc default-libmysqlclient-dev libcurl4-openssl-dev libssl-dev curl procps \
    # Cleaning cache:
    && apt autoremove -y \
    && apt autoclean -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir

COPY .  /django-project

WORKDIR /django-project
RUN pip install --compile "pycurl==7.45.2" #
RUN poetry install

WORKDIR /django-project/apps

ENV EXPOSE_PORT 8000
ENV UVICORN_WORKER_CNT 3

EXPOSE 8000
CMD gunicorn config.asgi:application --worker-class uvicorn.workers.UvicornWorker -w ${UVICORN_WORKER_CNT} --threads 3 -b 0.0.0.0:${EXPOSE_PORT}



