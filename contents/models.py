from django.db import models
from core.models import SoftDeleteModel, TimeStampMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Manager


class Category(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subcategories",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Post(SoftDeleteModel, TimeStampMixin):
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        # ordering = ('-created_at',)

    class Statuses(models.TextChoices):
        DRAFT = "D", _("Draft")
        PUBLISHED = "P", _("Published")
        UNPUBLISHED = "UP", _("Unpublished")

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    body = models.TextField(verbose_name=_("Body"), help_text=_("Post content"))
    category = models.ForeignKey(
        "contents.Category", on_delete=models.PROTECT, related_name="cat_posts"
    )
    publisher = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="pub_posts"
    )
    image = models.FileField(upload_to="uploads/posts/")
    status = models.CharField(
        max_length=2, choices=Statuses.choices, default=Statuses.DRAFT
    )

    def __str__(self) -> str:
        return self.title


class ArchievedPost(Post):
 
    objects = Manager()

    class Meta:
        proxy = True,
