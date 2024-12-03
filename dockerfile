FROM python:3.11.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev python3-pip git curl wget make build-essential \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
    libffi-dev && \
    pip3 install --upgrade pip poetry

# Set working directory
WORKDIR /home/lyvia/backend

# Configure poetry
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

# Copy configuration files first
COPY pyproject.toml poetry.lock Makefile config.toml ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application
COPY . .

# Install the project
RUN poetry install

# Set the default command to launch the app using make
CMD ["poetry", "run", "make", "launch"]