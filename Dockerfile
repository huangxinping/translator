FROM python:3.7.9

COPY . /app
WORKDIR /app
RUN pip install fastapi requests uvicorn lxml
EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "app:app" ] 