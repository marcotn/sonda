FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt update --fix-missing
RUN apt install -y build-essential curl ca-certificates gnupg2 lsb-release apt-utils

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null
RUN apt update
RUN apt upgrade -y
RUN apt install -y postgresql-client tzdata

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root

COPY . .
RUN python manage.py collectstatic --noinput

COPY boot.sh /boot.sh
RUN chmod +x /boot.sh
CMD ["/bin/bash", "/boot.sh"]
