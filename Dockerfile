FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /APP

WORKDIR /APP

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]