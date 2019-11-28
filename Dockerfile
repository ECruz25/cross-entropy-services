FROM python:3

LABEL Edwin Cruz "edwincruz255@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip unixodbc-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# RUN pip3 install numpy
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]