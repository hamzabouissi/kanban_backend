from django.db import models


class BaseModelWithLogicDelete(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract=True