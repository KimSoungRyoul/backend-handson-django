# [django-backend-starter Template]
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## django-backend-starter Docs
* https://kimsoungryoul.github.io/django-backend-starter/


## QuickStart

1. create virtualenv(venv) using poetry & install library
    ~~~shell
    poetry config virtualenvs.in-project true # if true .venv was created in PROJECT ROOT
    poetry shell
    poetry install
    ~~~

2. [Optional] install pre-commit config
   * if you want always run black&isort before commit
   ~~~shell
   pre-commit install
   ~~~
   * pre-commit run (reformatting)
   ~~~shell
   pre-commit run --files apps/**/**
   ~~~

3. [Optional] if you want to use not only sqlite3
   ~~~shell
   docker compose -f docker/compose.yaml up -d
   ~~~

4. django migration
    ~~~shell
    python apps/manage.py migrate
    ~~~

5. create superuser for test
   ~~~shell
   python apps/manage.py createsuperuser --username=root --email=kimsoungryoul@gmail.com
   ~~~

6. django runserver
    ~~~shell
    python apps/manage.py runserver 8000
    ~~~

7. you can see default API Docs in http://localhost:8000/docs

   <img src="./hello_django_backend_template.png" width="70%" height="50%">


## build
* install docker first [install docker desktop](https://www.google.com/search?q=docker+desktop&sourceid=chrome&ie=UTF-8)
1. docker build
   ~~~shell
   docker build -f docker/application.dockerfile -t django-backend-starter-application:1.0.0 .
   ~~~
2. docker run
   ~~~shell
   docker run -d -p "8000:8000" --rm --name django-backend-application django-backend-starter-application:1.0.0
   ~~~
