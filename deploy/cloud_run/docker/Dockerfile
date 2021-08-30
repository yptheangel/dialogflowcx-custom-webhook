FROM continuumio/miniconda3:latest

WORKDIR /app
COPY . /app
RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "run.sh"]