FROM python:3.5-slim

COPY . /app
WORKDIR /app

RUN \
    # install deps
    apt-get update -y && \
    pip install -e . -c requirements.txt && \
    pip install uwsgi \

    # cleanup
    rm -rf /var/lib/apt/lists/* && \

# Drop down to unprivileged user
USER webpush-channels

# Run uwsgi by default
CMD ["uwsgi", "--ini", "/etc/webpush-channels.ini"]