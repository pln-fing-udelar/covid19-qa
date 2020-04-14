## API Rest

## Server
Expone una API Rest

`docker-compose up api`


En `http://localhost:5000/` está la descripción swagger de los servicios y se puede interactuar.

### NOTAS:

1. No es necesario usar marshmallow, etc en este momento, pero si luego vamos a tener una BD puede ser más fácil dejarlo.
2. Definí los tipos Question, Answer, Feedback y Status para completar la definición de la API, esto debe traerse del modelo qué no estoy seguro como importar.
3. En particular no tengo ni idea como haríamos el Feedback, para poner algo lo dejé como que si el usuarios puntúa con True o False las respuestas de a una y el Feedback recibe esa lista. Quizá solo le pidamos al usuario puntuar la mejor y quizá no sea True o False. Esto hay que decidirlo.
4. El endpoint Test se puede sacar pero pensé que puede ser una forma de testear la recuperación de documentos.
5. Ejemplo de request para la query de Test (elasticsearch debe estar levantado):
```
{
  "number_of_fragments": 5,
  "fragment_size": 500,
  "result_size": 10,
  "text_field": "article_text",
  "query": "covid hola",
  "index_pattern": "covid*"
}
```