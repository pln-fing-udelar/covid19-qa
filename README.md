# COVID-19 QA

## Installation

1. Download [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Build the Docker images:

    ```bash
    docker-compose build
    ```

3. Create a super user and run the migrations for the `api` container:

    ```bash
    docker-compose run --rm api bash -c "python manage.py migrate; python manage.py createsuperuser"
    ```

## `qa` installation without Docker

**This option allows you use only the "testing" data because Elasticsearch (ES) is not installed**.

1. Setup the env. Install Miniconda (Linux setup; check online for MacOS and Windows):

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b
    ```

2. Open a new terminal after the installation.

    ```bash
    cd qa
    conda env create -f environment.yml
    conda activate covid19-qa
    ```

## Generate the corpus and upload the data into elastic search

1. Generate the XML article files from the JSON file:

    ```bash
    docker-compose up corpus-creator
    ```

2. Upload the data into ES using Logstash:

    ```bash
    docker-compose up logstash
    ```

## Start the `api` server

Start the `api` container in Docker Compose:

```bash
docker-compose up api
```

The Swagger description of the services is in http://localhost:8000/

## Interact with the model

The `qa` container has a `main.py` script with some commands useful to test the model. 
All the commands allow the flag `--ignore-es` to work with the testing data.

1. Go into the `qa` container.

    If the container is running:

    ```bash
    docker-compose exec qa bash
    ```
    
    If the container isn't running:

    ```bash
    docker-compose run qa bash
    ```

2. Inside the container, activate the conda env:

    ```bash
    conda activate covid19-qa
    ```

3. Execute the command. (Check out the help (`./main.py -h`) to see the available options.)
Some examples:

    ```bash
    # Execute the `try` with some optimizations:
    ./main.py --batch-size 672 --device 0 --threads 20
    # Execute the `try` with some optimizations and without Elasticsearch:
    ./main.py --batch-size 672 --device 0 --threads 20 --ignore-es
    # Execute the interactive mode:
    ./main.py interact
    # Execute the interactive mode and without Elastichsearch:
    ./main.py --ignore-es interact
    ```

## Query over Elasticsearch

A useful tool to interact with your elastic search cluster is [Kibana](https://www.elastic.co/kibana).

1. Run the Kibana container:

    ```bash
    docker-compose up kibana
    ```

2. In your browser, go to http://0.0.0.0:15601/app/kibana

## Make Docker work with Nvidia

The `qa` image is CUDA-enabled. It needs to run with the `nvidia` runtime to work well.

1. Install [nvidia-docker-runtime](https://github.com/NVIDIA/nvidia-container-runtime).

2. Run:

    ```bash
    sudo tee /etc/docker/daemon.json <<EOF
    {
        "runtimes": {
            "nvidia": {
                "path": "/usr/bin/nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "default-runtime": "nvidia"
    }
    EOF
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```

3. To test it (on a CUDA-enabled environment):

    ```bash
    docker-compose build qa
    docker-compose run --rm qa python -c "import torch; torch.ones(2, device='cuda')"
    ```

## Run Docker Compose in production mode

By default, Docker Compose will load both `docker-compose.yml` and `docker-compose.override.yml`.
In production mode, any `docker-compose` command must include the flags
`-f docker-compose.yml -f docker-compose.prod.yml`, like in:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

For it to work, you must first creat a `.env` file (filling with the env var values):

```dotenv
DB_PASS=<VALUE>
FLASK_SECRET_KEY=<VALUE>
POSTGRES_PASSWORD=<DB_PASS_VALUE>
SECRET_KEY=<VALUE>
TRAEFIK_EMAIL=<VALUE>
TRAEFIK_DOMAIN=<VALUE>
```

For every service you want exposed through the reverse proxy you should add this to the service block in `docker-compose.yml` file and change `SERVICE_NAME`:
```
depends_on:
  - traefik
networks:
  - proxy
labels:
  - traefik.http.routers.whoami.rule=Host(`SERVICE_NAME.${DOMAIN}`)
  - traefik.http.routers.whoami.tls=true
  - traefik.http.routers.whoami.tls.certresolver=le
```

This is an example service:

```
whoami:
    image: "containous/whoami"
    restart: always
    depends_on:
      - traefik
    networks:
      - proxy
    labels:
      - traefik.http.routers.whoami.rule=Host(`whoami.${DOMAIN}`)
      - traefik.http.routers.whoami.tls=true
      - traefik.http.routers.whoami.tls.certresolver=le
```

