FROM python:3.12

WORKDIR /book_managment

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /book_managment/

RUN poetry install --no-root

COPY . /book_managment

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]