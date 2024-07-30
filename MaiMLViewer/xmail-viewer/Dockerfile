FROM node:18-buster
MAINTAINER mnt

RUN apt-get update \
     && apt-get install -y python3-pip
#RUN pip3 install --upgrade setuptools
RUN pip3 install neo4j==4.4
RUN pip3 install lxml==5.0.0
RUN pip3 install cryptography==3.3.2
RUN pip3 install signxml==2.10.1

ADD xmail-viewer/bin /opt/app/xmail-viewer/bin
ADD xmail-viewer/common /opt/app/xmail-viewer/common
ADD xmail-viewer/models /opt/app/xmail-viewer/models
ADD xmail-viewer/routes /opt/app/xmail-viewer/routes
ADD xmail-viewer/views /opt/app/xmail-viewer/views
ADD xmail-viewer/app.js /opt/app/xmail-viewer/app.js
ADD xmail-viewer/package.json /opt/app/xmail-viewer/package.json
ADD graph-db/app/Cypher/cypher_api.js /opt/app/graph-db/app/Cypher/cypher_api.js
ADD graph-db/app/Script /opt/app/graph-db/app/Script
RUN mkdir -p /opt/app/xmail-viewer/models/tmp
RUN mkdir -p /opt/app/xmail-viewer/exports

ENV PORT 3000
ENV GRAPH_DB_IP 52.11.150.230

WORKDIR /opt/app/xmail-viewer
RUN npm i

EXPOSE 3000

CMD [ "node", "/opt/app/xmail-viewer/bin/www" ]
