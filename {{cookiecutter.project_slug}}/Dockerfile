##############################################
# Build virtualenv
##############################################
FROM python:{{cookiecutter.python_version}}-bullseye AS venv

# Prepare poetry
##############################################
# https://python-poetry.org/docs/#installation
ENV POETRY_VERSION={{cookiecutter.poetry_version}}
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH /root/.local/bin:$PATH

RUN python -m pip install --user poetry-lock-check==0.1.0 \
    cleo==0.8.1  # poetry-lock-check depends on cleo

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m poetry_lock_check check-lock

# Install python dependencies
##############################################
RUN python -m venv --copies /app/venv
# Will install dev deps as well, so that we can run tests in this image
RUN . /app/venv/bin/activate \
    && poetry install --no-interaction

ENV PATH /app/venv/bin:$PATH

# Collect static files & build assets
##############################################

COPY ./src /app/src
COPY ./envs/local-envs.env /app/.env
WORKDIR /app/src

# Required for manage.py to startup
ARG ENV_FILE=/app/.env
ARG DEBUG=true
ENV STATIC_ROOT=/app/static

RUN mkdir -p $STATIC_ROOT

# Build assets so that we don't need the build tools later
RUN python manage.py collectstatic --noinput --clear



##############################################
# write git info
##############################################
FROM alpine/git:v2.26.2 AS git

WORKDIR /app
COPY .git /app/.git/
RUN git describe --tags --always > /git-describe
RUN git rev-parse HEAD > /git-commit
RUN date +'%Y-%m-%d %H:%M %Z' > /build-date



##############################################
# Main image
##############################################
FROM python:{{cookiecutter.python_version}}-slim-bullseye AS final

ARG DEBIAN_FRONTEND=noninteractive

# Setup user & group
##############################################
RUN groupadd -g 1000 django
RUN useradd -M -d /app -u 1000 -g 1000 -s /bin/bash django

# Setup system
##############################################
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        libxml2 \
        media-types \
        postgresql-client

# Fetch project requirements
##############################################
COPY --chown=django:django --from=venv /app/venv /app/venv/
COPY --chown=django:django --from=git /git-describe /git-commit /build-date /app/git/
ENV PATH /app/venv/bin:$PATH

# Fetch built assets & static files
##############################################
ENV STATIC_ROOT=/app/static
COPY --chown=django:django --from=venv $STATIC_ROOT $STATIC_ROOT

# uWSGI env vars
##############################################
ENV UWSGI_HTTP=:8000
ENV UWSGI_CHDIR="/app/src"
ENV UWSGI_WSGI_FILE="/app/src/{{cookiecutter.project_slug}}/wsgi.py"

ENV UWSGI_MASTER=1
ENV UWSGI_HTTP_AUTO_CHUNKED=1
ENV UWSGI_HTTP_KEEPALIVE=1
ENV UWSGI_UID=1000
ENV UWSGI_GID=1000
ENV UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV UWSGI_DIE_ON_TERM=true
ENV UWSGI_STRICT=true
ENV UWSGI_NEED_APP=true

# Tweak for perf
ENV UWSGI_SINGLE_INTERPRETER=true
ENV UWSGI_AUTO_PROCNAME=true
ENV UWSGI_MAX_REQUESTS=5000
ENV UWSGI_MAX_WORKER_LIFETIME=3600
ENV UWSGI_RELOAD_ON_RSS=500
ENV UWSGI_WORKER_RELOAD_MERCY=10
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# Create directory structure
##############################################
WORKDIR /app
COPY pyproject.toml poetry.lock ./
ADD --chown=django:django ./src ./src
COPY --chown=django:django tasks.py ./tasks.py
COPY --chown=django:django docker/uwsgi.ini ./uwsgi.ini


RUN mkdir -p /app/data
RUN chown django:django /app /app/data

EXPOSE 8000

WORKDIR /app/src

USER django
CMD ["uwsgi", "--show-config", "--ini", "/app/uwsgi.ini"]
