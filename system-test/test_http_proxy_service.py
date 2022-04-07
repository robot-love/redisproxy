import os
import redis
import pytest
import requests
import multiprocessing as mp


def write_values_to_redis_db(kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.set(key, value)


def delete_values_from_redis_db(kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.delete(key)


@pytest.fixture(scope='module')
def keys_not_in_db():
    return [
        'not_in_db',
        'also_not_in_db',
        'also_not_in_db_either'
    ]


@pytest.fixture(scope="module", autouse=True)
def kv_pairs():
    kvs = {
        'name': 'Test',
        'number': '1234567890',
        'email': 'thing@now.com',
        'password': 'password',
        'password_confirm': 'password',
        'address': '123 Test St',
        'city': 'Testville',
        'state': 'CA',
        'zip': '12345',
        'phone': '1234567890',
        'card_number': '1234567890123456',
        'card_expiration': '12/20',
        'card_cvv': '123',
        'card_zip': '12345',
        'card_name': 'Test McTest',
        'card_type': 'Visa'
    }

    write_values_to_redis_db(kvs)
    yield kvs
    delete_values_from_redis_db(kvs)


def test_proxy_get_request_for_all_keys_in_db_finds_a_value(kv_pairs):
    for key, value in kv_pairs.items():
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.text is not "Key not found"


def test_proxy_get_request_for_all_keys_in_db_returns_a_non_empty_string(kv_pairs):
    for key, value in kv_pairs.items():
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.text != ""


def test_proxy_get_request_for_all_keys_returns_correct_values(kv_pairs):
    for key, value in kv_pairs.items():
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.text == value


def test_proxy_get_request_for_keys_in_db_returns_200(kv_pairs):
    for key, value in kv_pairs.items():
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.status_code == 200


def test_proxy_get_request_for_keys_not_in_db_returns_key_not_found(keys_not_in_db):
    for key in keys_not_in_db:
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.text == "Key not found"


def test_proxy_get_request_for_keys_not_in_db_returns_404(keys_not_in_db):
    for key in keys_not_in_db:
        r = requests.get(f'http://{os.environ["PROXY_HTTP_HOST"]}:{os.environ["PROXY_HTTP_PORT"]}/{key}')
        assert r.status_code == 404

