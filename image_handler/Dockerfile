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

#Build image_handler
FROM python-base as image_handler
ENV PYTHONPATH /app
ENV CONFIG_PATH /app/config.yaml
COPY --chown=test:test utils /app/utils
COPY --chown=test:test models /app/models
COPY --chown=test:test image_handler /app/image_handler
COPY --chown=test:test config.yaml /app/config.yaml
COPY --chown=test:test static /app/static
WORKDIR /app
USER test
CMD ["python3", "-u", "image_handler"]