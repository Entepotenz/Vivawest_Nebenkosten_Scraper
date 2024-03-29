# syntax=docker/dockerfile:1
FROM docker.io/library/alpine:latest as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH /usr/local/bin:$PATH

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

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

FROM docker.io/library/alpine:latest

# https://stackoverflow.com/questions/58701233/docker-logs-erroneously-appears-empty-until-container-stops
ENV PYTHONUNBUFFERED=1

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8
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
