FROM python:3
LABEL maintainer="mnt"

RUN pip install neo4jrestclient

WORKDIR /usr/src/app
COPY . .

ENV GRAPH_DB_IP 52.11.150.230
#ENV PYTHONIOENCODING=ja_JP.UTF-8

#日本語設定  
#RUN apt-get update
#RUN apt-get -y install locales && \
#    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
#ENV LANG ja_JP.UTF-8
#ENV LANGUAGE ja_JP:ja
#ENV LC_ALL ja_JP.UTF-8

CMD [ "sh", "./setup.sh" ]
