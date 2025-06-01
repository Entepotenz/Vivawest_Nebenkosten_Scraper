# syntax=docker/dockerfile:1@sha256:9857836c9ee4268391bb5b09f9f157f3c91bb15821bb77969642813b0d00518d
FROM docker.io/library/alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV PATH=/usr/local/bin:$PATH

ENV LANG=de_DE.UTF-8
ENV LC_ALL=de_DE.UTF-8

RUN apk add --no-cache \
  python3 \
  python3-dev \
  py3-pip \
  poetry \
  build-base \
  #    musl-locales \
  #    musl-locales-lang \
  && rm -rf /var/cache/apk/*

RUN python3 --version; \
  pip3 --version; \
  poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export --without dev --format=requirements.txt | pip install --no-cache-dir --target=/dependencies -r /dev/stdin;

FROM docker.io/library/alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# https://stackoverflow.com/questions/58701233/docker-logs-erroneously-appears-empty-until-container-stops
ENV PYTHONUNBUFFERED=1

ENV LANG=de_DE.UTF-8
ENV LC_ALL=de_DE.UTF-8
#ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

RUN addgroup --system python && \
  adduser -S -s /bin/false -G python python

RUN apk add --no-cache \
  python3 \
  chromium-chromedriver \
  #    musl-locales \
  #    musl-locales-lang \
  && rm -rf /var/cache/apk/*

COPY --chown=python:python --from=builder /dependencies /usr/local
ENV PYTHONPATH=/usr/local

RUN python3 --version

WORKDIR /app

COPY --chown=python:python source/ /app/source/

USER python

CMD ["sh", "-c", "source /app/pass.sh; python source/main.py json"]
#CMD ["sh", "-c", "source /app/pass.sh; python source/main.py"]
#CMD ["sh", "-c", "source /app/pass.sh; python -m pytest source/tests/"]
