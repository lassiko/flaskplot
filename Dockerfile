FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
RUN apk add --no-cache tzdata
ENV TZ Europe/Helsinki
CMD python ./app.py