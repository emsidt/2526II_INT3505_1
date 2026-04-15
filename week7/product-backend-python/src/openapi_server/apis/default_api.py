# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

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


@router.get(
    "/products",
    responses={
        200: {"description": "Product list"},
    },
    tags=["default"],
    summary="Get all products",
    response_model_by_alias=True,
)
async def products_get(
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().products_get()


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
    product_input: ProductInput = Body(None, description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().products_post(product_input)


@router.get(
    "/product/{id}",
    responses={
        200: {"description": "Product found"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Get product by id",
    response_model_by_alias=True,
)
async def product_id_get(
    id: StrictStr = Path(..., description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().product_id_get(id)


@router.put(
    "/product/{id}",
    responses={
        200: {"description": "Product updated"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Update product",
    response_model_by_alias=True,
)
async def product_id_put(
    id: StrictStr = Path(..., description=""),
    product_input: ProductInput = Body(None, description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().product_id_put(id, product_input)


@router.delete(
    "/product/{id}",
    responses={
        200: {"description": "Product deleted"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="delete product",
    response_model_by_alias=True,
)
async def product_id_delete(
    id: StrictStr = Path(..., description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().product_id_delete(id)
