FROM python:3-alpine

COPY api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY api .
EXPOSE 8080
ENTRYPOINT gunicorn -c config.py main:app
