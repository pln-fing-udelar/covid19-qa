## Jupyter

### Ejecución

`docker-compose up elasticsearch-covid`

El servicio elasticsearch-covid es dependencia de logstash y jupyter y no es necesario levantarlo de manera independiente.

La api de elasticsearch queda disponible en http://localhost:9200 desde el equipo host y desde los demás servicios de docker como logstash y jupyter queda disponible en http://elasticsearch-covid:9200