FROM python

ENV TERM=xterm
ENV LANG en_US.UTF-8

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt


ADD . /usr/src/

WORKDIR /usr/src/app


CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "wsgi:app", "--preload"]
