FROM python:3.7-alpine as base

COPY app/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]