FROM python:3-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# rustc compiler would be needed on ARM type devices but theres an issue with some deps not building..
ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1

ENV PATH /usr/local/bin:$PATH

RUN apt-get update && \
    apt-get install -y locales --no-install-recommends && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

# install system dependencies
#   the python cryptography package needs to be compiled for raspberrypi -> need gcc, rustc and libssl-dev
RUN apt-get update \
    && apt-get -y install gcc make libssl-dev libffi-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*s

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip

RUN python3 --version
RUN pip3 --version

RUN pip install --target=/dependencies -r /requirements.txt

FROM python:3-slim

# https://stackoverflow.com/questions/58701233/docker-logs-erroneously-appears-empty-until-container-stops
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y locales --no-install-recommends && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

# install chromium
RUN apt-get update \
    && apt-get -y install chromium chromium-driver --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*s

COPY --from=builder /dependencies /usr/local
ENV PYTHONPATH=/usr/local

RUN python3 --version

WORKDIR /app

CMD ["bash", "-c", "source /app/pass.sh; python source/main.py json"]
# CMD ["bash", "-c", "source /app/pass.sh; python source/main.py"]
