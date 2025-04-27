FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY scraper/ scraper/

ENTRYPOINT ["poetry", "run", "python", "-m", "scraper"]
