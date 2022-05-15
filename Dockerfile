FROM python:3.9

WORKDIR /EsferasSoftware

COPY ./requirements.txt /EsferasSoftware/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /EsferasSoftware/requirements.txt

COPY ./app /EsferasSoftware/app

COPY ./README.md /EsferasSoftware/README.md

WORKDIR /EsferasSoftware/app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
