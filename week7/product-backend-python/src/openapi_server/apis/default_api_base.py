# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from typing import Any
from openapi_server.models.product_input import ProductInput


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def products_get(
        self,
    ) -> None:
        ...


    async def products_post(
        self,
        product_input: ProductInput,
    ) -> None:
        ...


    async def product_id_get(
        self,
        id: StrictStr,
    ) -> None:
        ...


    async def product_id_put(
        self,
        id: StrictStr,
        product_input: ProductInput,
    ) -> None:
        ...


    async def product_id_delete(
        self,
        id: StrictStr,
    ) -> None:
        ...
