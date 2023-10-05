FROM python:3.10

RUN apt-get update
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG INSTALL_ARGS="--no-root"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
#RUN pip install poetry
#COPY pyproject.toml poetry.lock .env ./
#
#RUN poetry config virtualenvs.create false \
#    && poetry install $INSTALL_ARGS
COPY requirements.txt .env ./
RUN pip install -r requirements.txt


#COPY entrypoint.sh /code/entrypoint.sh
#RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
ENV PYTHONPATH=/code