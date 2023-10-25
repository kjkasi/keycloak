FROM kjkasi/python-alpine:231023

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/app

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]