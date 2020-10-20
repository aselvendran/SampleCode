FROM python:3.6

WORKDIR /usr

COPY requirements.txt /usr/requirements.txt
VOLUME /usr/saved_data
RUN pip install -r requirements.txt
COPY . /usr
