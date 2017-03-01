FROM python:3.5-slim

COPY . /app
WORKDIR /app

RUN buildDeps=' \
    libpq-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    ' && \
    # install deps
    apt-get update -y && \
    apt-get install -y --no-install-recommends $buildDeps && \
    pip install -e . -c requirements.txt && \
    pip install uwsgi && \

    # cleanup
    apt-get purge -y $buildDeps && \
    rm -rf /var/lib/apt/lists/* && \

# Drop down to unprivileged user
USER webpush-channels

# Run uwsgi by default
CMD ["uwsgi", "--ini", "/etc/webpush-channels.ini"]