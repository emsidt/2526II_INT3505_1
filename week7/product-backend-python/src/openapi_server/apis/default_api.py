# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl
from bson import ObjectId
from openapi_server.db import products_collection
from fastapi import APIRouter, Body, HTTPException

from openapi_server.db import products_collection
from openapi_server.models.product_input import ProductInput

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import StrictStr
from typing import Any
from openapi_server.models.product_input import ProductInput


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

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


@router.get(
    "/products",
    responses={
        200: {"description": "Product list"},
    },
    tags=["default"],
    summary="Get all products",
    response_model_by_alias=True,
)
async def products_get() -> list:
    products = []
    cursor = products_collection.find()

    async for product in cursor:
        products.append(product_serializer(product))

    return products


@router.post(
    "/products",
    responses={
        201: {"description": "Product created"},
    },
    tags=["default"],
    summary="Create product",
    response_model_by_alias=True,
)
async def products_post(
    product_input: ProductInput = Body(...),
) -> dict:
    product_data = product_input.model_dump(exclude_none=True)

    result = await products_collection.insert_one(product_data)

    new_product = await products_collection.find_one(
        {"_id": result.inserted_id}
    )

    return product_serializer(new_product)

@router.get(
    "/products/{id}",
    responses={
        200: {"description": "Product found"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Get product by id",
    response_model_by_alias=True,
)
async def products_id_get(
    id: str,
) -> dict:
    object_id = to_object_id(id)

    product = await products_collection.find_one({"_id": object_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_serializer(product)

@router.put(
    "/products/{id}",
    responses={
        200: {"description": "Product updated"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Update product",
    response_model_by_alias=True,
)
async def products_id_put(
    id: str,
    product_input: ProductInput = Body(...),
) -> dict:
    object_id = to_object_id(id)
    product_data = product_input.model_dump(exclude_none=True)

    result = await products_collection.update_one(
        {"_id": object_id},
        {"$set": product_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await products_collection.find_one({"_id": object_id})

    return product_serializer(updated_product)

@router.delete(
    "/products/{id}",
    responses={
        200: {"description": "Product deleted"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="delete product",
    response_model_by_alias=True,
)
@router.delete(
    "/products/{id}",
    responses={
        200: {"description": "Product deleted"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Delete product",
    response_model_by_alias=True,
)
async def products_id_delete(
    id: str,
) -> dict:
    object_id = to_object_id(id)

    result = await products_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}