FROM python:3.6

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    gcc \
    gdal-bin \
    gettext \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /src
WORKDIR /src

COPY requirements.txt /src

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY external_api /src/external_api
COPY questions /src/questions
COPY management /src/management
COPY manage.py /src
COPY wsgi.py /src
EXPOSE 8000

CMD ["uwsgi", "--http", ":8000", "--wsgi-file", "wsgi.py"]
