FROM python:3.10-slim

COPY ./ /app/src

WORKDIR /app/src

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

CMD uvicorn main:API --host=0.0.0.0 --port 8000
