## Logstash

### Ejecución

`docker-compose up logstash-covid`

Logstash va a indexar los archivos cada vez que sea ejecutado, puede configurarse para detectar nuevos archivos cada X tiempo.

### Explicación

Logstash enviará el template `template.json` a elasticsearch. Ese template indica como serán indexados los campos. Todos los campos son indexados sin cambios exepto el campo `article_text`, para el cual se crearán los siguientes "fields":

1. `article_text` es un campo que aplica el analyzer "covid-analyzer" que consiste en:
* lowercase
* asciifolding
* remove-stopwords
* change-synonyms

2. `article_text.raw` es el campo de texto sin cambios