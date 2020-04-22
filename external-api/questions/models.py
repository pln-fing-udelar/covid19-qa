from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    CORRECT = 1
    WRONG = 2
    FAKE = 3

    FEEDBACK_CHOICES = (
        (CORRECT, 'Respuesta Correcta'),
        (WRONG, 'Respuesta Incorrecta'),
        (FAKE, 'Noticia Falsa')
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    context = models.TextField()
    answer = models.CharField(max_length=500, blank=True)
    feedback = models.IntegerField(choices=FEEDBACK_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.answer

