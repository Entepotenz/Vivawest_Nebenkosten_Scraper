FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH /usr/local/bin:$PATH

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

# install system dependencies
#   the python cryptography package needs to be compiled for raspberrypi -> need gcc, rustc and libssl-dev
RUN apt-get update \
    && apt-get -y install gcc make rustc libssl-dev \
    && rm -rf /var/lib/apt/lists/*s

# installl chromium
RUN apt-get update \
    && apt-get -y install chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*s

RUN python3 --version
RUN pip3 --version

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install --no-dev

RUN apt-get -y remove gcc make rustc libssl-dev

COPY . .

CMD ["bash", "-c", "source /app/pass.sh; poetry run python source/main.py json"]