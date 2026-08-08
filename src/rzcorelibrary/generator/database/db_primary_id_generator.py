# File Name: rz-core-libarary/src/rzcorelibrary/generator/database/db_primary_id_generator.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

from django.db import models
from ..general.unique_int_id import UniqueIntId

class DbPrimaryIdGenerator:

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} cannot be instantiated."
        )

    @staticmethod
    def get_bigint_id(
            model_class: type[models.Model],
            column_name: str = "id",
            length: int = 36,
            is_start_with_zero: bool = True
    ) -> int:

        pk_id = UniqueIntId.get_bigint_id(length, is_start_with_zero)
        while (
                model_class.objects.filter(
                    **{column_name: pk_id}
                ).exists()
        ):
            pk_id = UniqueIntId.get_bigint_id(length, is_start_with_zero)

        return pk_id

class Plugin(BasePlugin):
    name = "db_primary_id_generator"
    version = "1.0.0"
    description = "Database primary ID generator"

    def get_util(self):
        return DbPrimaryIdGenerator