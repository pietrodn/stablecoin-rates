FROM python:3.10

ENV POETRY_VIRTUALENVS_IN_PROJECT=1 PYTHONUNBUFFERED=1
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY ./stablecoin_rates/__init__.py ./stablecoin_rates/__init__.py
RUN poetry install --no-dev

COPY stablecoin_rates ./stablecoin_rates

CMD [".venv/bin/python", "./stablecoin_rates/telegram/bot.py"]
