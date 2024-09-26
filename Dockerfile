# syntax=docker/dockerfile:1@sha256:865e5dd094beca432e8c0a1d5e1c465db5f998dca4e439981029b3b81fb39ed5
FROM docker.io/library/alpine:3.20.1@sha256:b89d9c93e9ed3597455c90a0b88a8bbb5cb7188438f70953fede212a0c4394e0 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH=/usr/local/bin:$PATH

ENV LANG=de_DE.UTF-8
ENV LC_ALL=de_DE.UTF-8

RUN apk add --no-cache \
  python3 \
  python3-dev \
  py3-pip \
  build-base \
  #    musl-locales \
  #    musl-locales-lang \
  && rm -rf /var/cache/apk/*

COPY requirements.txt /requirements.txt

RUN python3 --version; pip3 --version

RUN pip install --no-cache-dir --target=/dependencies -r /requirements.txt

FROM docker.io/library/alpine:3.20.1@sha256:b89d9c93e9ed3597455c90a0b88a8bbb5cb7188438f70953fede212a0c4394e0

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
