# syntax=docker/dockerfile:1@sha256:e87caa74dcb7d46cd820352bfea12591f3dba3ddc4285e19c7dcd13359f7cefd
FROM docker.io/library/alpine:3.20.2@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5 AS builder

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

FROM docker.io/library/alpine:3.20.2@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

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
