# File Name: rz-core-libarary/src/rzcorelibrary/generator/database/db_slug_generator.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

from typing import Optional

from django.db import models
from django.utils.text import slugify

class DbSlugGenerator:

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} cannot be instantiated."
        )

    @staticmethod
    def generate(
            model_class: type[models.Model],
            value: Optional[str],
            column_name: str = "slug",
    ) -> str:
        if value is None:
            return ""

        value = value.strip().lower()

        if not value:
            return ""

        base_slug = slugify(value)

        if not base_slug:
            return ""

        queryset = model_class.objects.all()

        slug = base_slug
        counter = 1

        while model_class.objects.filter(**{column_name: slug}).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

class Plugin(BasePlugin):
    name = "db_slug_generator"
    version = "1.0.0"
    description = "Generate unique slug for Django model"
    def get_util(self):
        return DbSlugGenerator