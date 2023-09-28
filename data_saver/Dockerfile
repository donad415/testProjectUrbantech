FROM python:3.10-alpine as python-base
RUN addgroup -S test && adduser -S test -G test
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY requirements.txt /tmp/requirements.txt
RUN apk update && \
    apk upgrade && \
    apk add --update --no-cache \
    bash \
    wget \
    postgresql-libs && \
    apk add --update --no-cache -t .build-deps \
    postgresql-dev \
    build-base


RUN pip3 install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

#Build data_saver
FROM python-base as data_saver
ENV PYTHONPATH /app
ENV CONFIG_PATH /app/config.yaml
RUN mkdir -p /uploads \ && chown -R test:test /uploads
COPY --chown=test:test utils /app/utils
COPY --chown=test:test models /app/models
COPY --chown=test:test data_saver /app/data_saver
COPY --chown=test:test config.yaml /app/config.yaml
WORKDIR /app
USER test
CMD ["python3", "-u", "data_saver"]