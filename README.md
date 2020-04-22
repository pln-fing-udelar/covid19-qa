# COVID-19 QA

## Installation

1. Download [the model](https://drive.google.com/drive/folders/1K-eXgmXytoIELHI8Rq3_dP9BUujBQ9T2?usp=sharing) in `model/`.
2. Download [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).
3. Build the docker images
```bash
docker-compose build
```
4. Create a super user and run the migrations for the external-api container
```bash
docker-compose run external-api bash

# Inside the container:
python manage.py migrate
python manage.py createsuperuser
```

## Installation without docker

**This option allows you use only the "testing" data beacuse elasticsearch is not installed**.

1. Setup the env. Install Miniconda (Linux setup; check online for MacOS and Windows):

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash -b Miniconda3-latest-Linux-x86_64.sh
    ```

2. Open a new terminal after the installation.

    ```bash
    cd qa
    conda env create -f environment.yml
    conda activate covid19-qa
    ```

## Generate the corpus and upload the data into elastic search

1. Generate the xml from the json
```bash
docker-compose up corpus-creator-covid
```

2. Upload the data into ES using logstah
```bash
docker-compose up logstash-covid
```

## Start the api server

1. Start the qa container in docker
```bash
docker-compose up -d external-api
```

The swagger description of the services is in http://localhost:5000/


## Interact with the model

The qa-covid container has a `main.py` script with some commands useful to test the model. 
All the commands allow the flag `--ignore-es` to work with the testing data.

1. Go into the `qa-covid` container.
If the container is runnig
```bash
docker-compose exec qa-covid bash
```

If the containar is not running
```bash
docker-compose run qa-covid bash
```

2. Inside the container, activate the conda env.
```bash
conda activate covid19-qa
```

3. Execute the command. (Check out the help (`./main.py -h`) to see the available options.)
Some examples:
```bash
# Execute the `try` with some optimizations
./main.py --batch-size 672 --device 0 --threads 20
# Execute the `try` with some optimizations without ES
./main.py --batch-size 672 --device 0 --threads 20 --ignore-es True
# Execute the interactive mode
./main.py interact
# Execute the interactive mode without ES
./main.py --ignore-es True interact
```

## Query over elastic search
A useful tool to interact with your elastic search cluster is [Kibana](https://www.elastic.co/kibana)

1. Run the kibana container
```bash
docker-compose up kibana-covid
```
2. In your browser, go to http://0.0.0.0:15601/app/kibana