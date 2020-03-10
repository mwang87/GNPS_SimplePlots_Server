FROM ubuntu:18.04
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

RUN pip3 install flask
RUN pip3 install gunicorn
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install requests_cache
RUN pip3 install plotnine

COPY . /app
WORKDIR /app