FROM pytorch/pytorch:1.5-cuda10.1-cudnn7-runtime

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["bash", "-c"]

EXPOSE 5000

COPY api covid19_qa *.py ./

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
CMD source activate covid19-qa && flask run -h 0.0.0.0
