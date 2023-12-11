from django.db import models
# from uuid import uuid4
from django.db.models.query import QuerySet


class BaseModel(models.Model):
    # id = models.UUIDField(editable=False, primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class MyManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)

    def archives(self):
        return super().get_queryset().filter(is_active=False)


class SoftDeleteModel(BaseModel):
    objects = MyManager()

    is_active = models.BooleanField(default=True, db_index=True)

    def delete(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True


class TimeStampMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)