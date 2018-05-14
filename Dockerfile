FROM alpine

CMD ["python3", "run.py"]

WORKDIR /src

RUN apk add --update python3
RUN apk add --no-cache --virtual .build-deps build-base python3-dev py3-pip \
    && pip3 --no-cache install apscheduler aiodocker \
    https://github.com/squeaky-pl/japronto/archive/master.zip \
	&& apk del .build-deps \
	&& rm -rf /var/cache/apk/*

ADD *.py ./
