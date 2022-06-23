ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 \
    py3-pip
RUN \
  python3 -m pip install Flask requests

WORKDIR /data

COPY server.py /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]