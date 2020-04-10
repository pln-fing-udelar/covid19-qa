# COVID-19 QA

## Installation

1. Setup the env. Install Miniconda (Linux setup; check online for MacOS and Windows):

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash -b Miniconda3-latest-Linux-x86_64.sh
    ```

2. Open a new terminal after the installation.

    ```bash
    conda env create -f environment.yml
    conda activate covid19-qa
    ```

3. Download [the model](https://drive.google.com/drive/folders/1K-eXgmXytoIELHI8Rq3_dP9BUujBQ9T2?usp=sharing) in `model/`.

## Run

```bash
./main.py
```

Check out the help (`./main.py -h`) to see the available options.

### Run with some optimizations

```bash
./main.py --batch-size 672 --device 0 --threads 20
```

## Elastic Search

TODO

### With Docker & Docker Compose

TODO

### With Docker

TODO
