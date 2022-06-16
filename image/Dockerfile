FROM python:3.9-slim-bullseye

RUN apt-get update
RUN apt-get install -y libgomp1 git libquadmath0

WORKDIR /usr/src/app

COPY run.py ../run.py

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD cp config/.env .env && pip install -r repository/requirements.txt && python ../run.py