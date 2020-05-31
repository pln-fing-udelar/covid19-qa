from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
class QueryConf(models.Model):
    parameter_name = models.CharField(unique=True, max_length=100)
    conf = JSONField()

    def __str__(self):
        return self.parameter_name
