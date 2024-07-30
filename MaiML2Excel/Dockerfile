FROM python:3

RUN apt-get update && \
    apt-get install -y python3-pip
RUN pip install --upgrade pip  && \
    pip install jupyterlab  && \
    pip install openpyxl
RUN pip install xmltodict
#RUN mkdir -p /WORK/DATA/INPUT
#RUN mkdir -p /WORK/DATA/OUTPUT
#RUN mkdir -p /WORK/DATA/TMP
