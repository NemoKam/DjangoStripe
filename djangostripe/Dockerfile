FROM python:3.13.3-bookworm

WORKDIR /djangostripe

COPY requirements.txt /djangostripe/

RUN apt clean -y
RUN apt update -y
RUN apt install dos2unix -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /djangostripe/

RUN chmod u+x /djangostripe/entrypoint.sh
RUN chmod u+x /djangostripe/prepare_db.sh

RUN dos2unix /djangostripe/entrypoint.sh
RUN dos2unix /djangostripe/prepare_db.sh

CMD ["./entrypoint.sh"]
