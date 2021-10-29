FROM python:3.9

WORKDIR /code

COPY ./store.db /code/store.db

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]