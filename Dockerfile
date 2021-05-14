FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /APP

WORKDIR /APP

RUN pip install --upgrade pip

RUN pip install -r requirements.txt