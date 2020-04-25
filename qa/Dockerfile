FROM continuumio/miniconda3
WORKDIR /src

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
CMD ["conda", "run", "-n", "covid19-qa", "gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "wsgi:app", "--preload"]
