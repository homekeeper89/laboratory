FROM python:3.8.6

COPY . .
WORKDIR /app

# RUN apk update && apk add python3-dev libffi-dev gcc
RUN pip install --upgrade pip setuptools
# RUN pip install cryptography==3.2.1
RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 5000

# WORKDIR /
# CMD ["python", "main.py"]