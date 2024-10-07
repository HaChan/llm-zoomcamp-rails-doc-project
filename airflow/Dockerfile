FROM apache/airflow:2.7.1-python3.11

USER root

RUN apt-get update

USER airflow

COPY requirement.txt /
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirement.txt
