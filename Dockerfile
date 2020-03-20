FROM tiangolo/uwsgi-nginx:python3.6



RUN apt-get update && \
    apt-get install python3 python3-pip python3-flask \
    unixodbc-dev libpq-dev pkg-config libcairo2-dev libglib2.0-dev \
    build-essential libssl-dev libffi-dev libgirepository1.0-dev\
    libxml2-dev libxslt1-dev zlib1g-dev libcairo2 \
    python-pip -y

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt



