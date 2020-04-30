FROM python:3.6

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN apt-get update && apt-get install -y \
        vim \
        gcc \
	    gdal-bin \
        gettext \
        postgresql-client \
        --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /src
WORKDIR /src

COPY requirements.pip /src

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.pip

COPY external_api /src
COPY questions /src
COPY manage.py /src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
