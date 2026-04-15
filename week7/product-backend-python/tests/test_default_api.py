# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from openapi_server.models.product_input import ProductInput  # noqa: F401


def test_products_get(client: TestClient):
    """Test case for products_get

    Get all products
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_post(client: TestClient):
    """Test case for products_post

    Create product
    """
    product_input = {"price":0.8008281904610115,"name":"name","description":"description","category":"category","stock":6}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/products",
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_product_id_get(client: TestClient):
    """Test case for product_id_get

    Get product by id
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/product/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_product_id_put(client: TestClient):
    """Test case for product_id_put

    Update product
    """
    product_input = {"price":0.8008281904610115,"name":"name","description":"description","category":"category","stock":6}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/product/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_product_id_delete(client: TestClient):
    """Test case for product_id_delete

    delete product
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/product/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

