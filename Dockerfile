FROM python:alpine

ADD . .

WORKDIR .

RUN pip3 install -r requirements.txt

CMD ["python3", "smarthome_hs110.py"]