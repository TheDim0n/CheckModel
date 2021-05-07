FROM python:3.7.9-slim

COPY ./ /APP

WORKDIR /APP

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]