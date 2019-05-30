FROM python:alpine

ADD app ./app
ADD config.py .
ADD smarthome_hs110.py .
ADD requirements.txt .

WORKDIR .

RUN pip3 install -r requirements.txt

CMD ["python3", "smarthome_hs110.py"]
