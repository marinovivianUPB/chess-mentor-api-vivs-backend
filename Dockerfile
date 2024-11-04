FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./docs /code/docs
COPY ./src /code/src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]