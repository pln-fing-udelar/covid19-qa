FROM nvidia/driver:440.64.00-ubuntu18.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    wget \
  && rm -rf /var/lib/apt/lists/* \
  && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
  && bash Miniconda3-latest-Linux-x86_64.sh -b \
  && rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH /root/miniconda3/condabin:/root/miniconda3/bin:$PATH

COPY environment.yml .
RUN conda env create -f environment.yml

EXPOSE 5000

COPY *.py ./
COPY api ./api
COPY covid19_qa ./covid19_qa

# PyTorch has particular ways in which multiple processes share CUDA tensors.
# This gives problems with gunicorn workers (even if you have 1 worker and 1 thread; a sync worker).
# Plus, even if it's all thread-safe, in this use case we better use all the GPU we can for every question
# (largest batch size possible; we try to check with all the document fragments we can).
# We then can just run this sync.
#
# So, it makes sense just to use Flask server in production.
# The problems with flask in production are about the response time and scalability,
# which we don't care because we're just running sync.
# Another problem could be the security risk of enabling debug mode in production.
# Let's just avoid that with the env var and that's it.
# See https://stackoverflow.com/a/12269934/1165181

SHELL ["bash", "-c"]

# Override nvidia/driver default.
ENTRYPOINT []

CMD source activate covid19-qa && flask run -h 0.0.0.0
