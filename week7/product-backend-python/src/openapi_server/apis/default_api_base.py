# coding: utf-8

from typing import ClassVar, Tuple

from bson import ObjectId
from fastapi import HTTPException
from pydantic import StrictStr

from openapi_server.db import products_collection
from openapi_server.models.product_input import ProductInput


def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product.get("name"),
        "price": product.get("price"),
        "description": product.get("description"),
        "category": product.get("category"),
        "stock": product.get("stock"),
    }


def to_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid product id")
    return ObjectId(id)


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)

    async def products_get(
        self,
    ) -> list:
        products = []
        cursor = products_collection.find()

        async for product in cursor:
            products.append(product_serializer(product))

        return products

    async def products_post(
        self,
        product_input: ProductInput,
    ) -> dict:
        product_data = product_input.model_dump(exclude_none=True)

        result = await products_collection.insert_one(product_data)

        new_product = await products_collection.find_one(
            {"_id": result.inserted_id}
        )

        return product_serializer(new_product)

    async def products_id_get(
        self,
        id: StrictStr,
    ) -> dict:
        object_id = to_object_id(id)

        product = await products_collection.find_one(
            {"_id": object_id}
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product_serializer(product)

    async def products_id_put(
        self,
        id: StrictStr,
        product_input: ProductInput,
    ) -> dict:
        object_id = to_object_id(id)
        product_data = product_input.model_dump(exclude_none=True)

        result = await products_collection.update_one(
            {"_id": object_id},
            {"$set": product_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        updated_product = await products_collection.find_one(
            {"_id": object_id}
        )

        return product_serializer(updated_product)

    async def products_id_delete(
        self,
        id: StrictStr,
    ) -> dict:
        object_id = to_object_id(id)

        result = await products_collection.delete_one(
            {"_id": object_id}
        )

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "message": "Product deleted"
        }