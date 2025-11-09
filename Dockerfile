FROM python:3.13

WORKDIR /qaguru2

RUN pip install poetry

COPY pyproject.toml poetry.lock* /qaguru2/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

COPY ./app /qaguru2/app
COPY users.json /qaguru2/

CMD ["fastapi", "run", "app/main.py", "--port", "80"]