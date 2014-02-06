from django.db import models
from django.contrib.auth.models import User


class ProgramFile(models.Model):
    name = models.CharField(max_length=30, default="no_name")
    data = models.TextField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def get_data(self):
        return self.data