from tabnanny import verbose
from turtle import ondrag

from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


# Create your models here.
class Category(MPTTModel):
    """Inventory Category tables implemented with MPTT"""

    name = models.CharField(max_length=100, verbose_name=_("category name"), help_text=_("format: required, max-100"))
    slug = models.SlugField(
        max_length=100,
        verbose_name=_("category safe ulr"),
        help_text=_("format: required, letters, numbers, underscore, or hypens"),
    )
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("parent of category"),
        help_text=_("format: not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name
