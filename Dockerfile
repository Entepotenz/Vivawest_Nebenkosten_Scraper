FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc make \
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

COPY . .

CMD ["bash", "-c", "source /app/pass.sh; poetry run python source/main.py"]