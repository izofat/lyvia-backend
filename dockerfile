FROM python:3.11.11-bookworm

RUN apt-get update && apt-get install -y \
    python3-dev python3-pip git curl wget make build-essential \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
    libffi-dev && \
    pip3 install --upgrade pip poetry

WORKDIR /home/lyvia/backend

COPY pyproject.toml poetry.lock Makefile config.toml ./

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project false && \
    poetry install

COPY . /home/lyvia/backend

CMD ["poetry", "run", "make", "launch"]
