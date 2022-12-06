FROM python:3.10-alpine
LABEL maintainer "danianmercado@gmail.com" 
COPY . /
RUN pip3 install cloudscraper kafka-python colorama python-dotenv
RUN crontab ./crontab
CMD ["crond", "-f"]
