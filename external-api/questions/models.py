from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=500, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    CORRECT = 1
    WRONG = 2
    FAKE = 3
    PARTIAL = 4

    FEEDBACK_CHOICES = (
        (CORRECT, 'Respuesta Correcta'),
        (WRONG, 'Respuesta Incorrecta'),
        (FAKE, 'Noticia Falsa'),
        (PARTIAL, 'Respuesta Parcialmente Correcta')
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    context = models.TextField()
    answer = models.CharField(max_length=500, blank=True)
    feedback = models.IntegerField(choices=FEEDBACK_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prob = models.FloatField(null=True)

    def __str__(self):
        return self.answer
