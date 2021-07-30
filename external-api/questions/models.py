from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=500, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    
    NO_MATCH = 1
    INCOMPLETE_MATCH = 2
    CONTAINED_MATCH = 3
    EXACT_MATCH = 4

    UNRELATED_PARAGRAPHS = 1
    RELATED_PARAGRAPHS = 2
    GOOD_PARAGRAPHS = 3

    ANSWER_FEEDBACK_CHOICES = (
        (EXACT_MATCH, 'Respuesta Correcta'),
        (CONTAINED_MATCH, 'Respuesta Contenida'),
        (INCOMPLETE_MATCH, 'Respuesta Incompleta'),
        (NO_MATCH, 'Respuesta incorrecta')
    )

    PARAGRAPH_FEEDBACK_CHOICES = (
        (UNRELATED_PARAGRAPHS, 'No relacionado'),
        (RELATED_PARAGRAPHS, 'Relacionado'),
        (GOOD_PARAGRAPHS, 'Contiene respuesta')
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    context = models.TextField()
    answer = models.CharField(max_length=500, blank=True)
    answer_feedback = models.IntegerField(choices=ANSWER_FEEDBACK_CHOICES, blank=True, null=True)
    paragraph_feedback = models.IntegerField(choices=PARAGRAPH_FEEDBACK_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer
