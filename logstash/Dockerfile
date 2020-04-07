# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:7.6.0
# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-filter-rest

RUN curl https://jdbc.postgresql.org/download/postgresql-42.2.10.jar --output /usr/share/logstash/logstash-core/lib/jars/postgresql-42.2.10.jar
COPY config/logstash.yml /usr/share/logstash/config/logstash.yml
COPY template.json /etc/logstash/templates/template.json
COPY pipeline /usr/share/logstash/pipeline
RUN mkdir /tmp/datos
ADD datos /tmp/datos
USER root
RUN chown -R logstash:logstash /tmp/datos
RUN chmod -R 777 /tmp/datos