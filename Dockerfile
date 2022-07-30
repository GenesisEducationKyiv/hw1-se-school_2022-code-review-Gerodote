FROM python:3.10-slim

COPY ./ /app/src

WORKDIR /app/src

# RUN apt-get update
# RUN apt-get -y install telnet
# RUN apt-get -y install gcc rustc libc6-dev linux-headers-5.10.0-12-amd64 
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

# VOLUME [ "/" ]

CMD uvicorn main:API --host=0.0.0.0 --port 8000
