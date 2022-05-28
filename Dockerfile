FROM alpine:3.16

RUN apk add --update --no-cache python3 py3-requests

ADD dl_dd.py /dl_dd.py

VOLUME /data

CMD while true; do /dl_dd.py > /data/dd_meshviewer.json; sleep 60; done

