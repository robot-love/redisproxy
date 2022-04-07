import os
import redis
import pytest
import multiprocessing as mp
from redis.exceptions import ResponseError


def write_values_to_redis_db(redis_client, kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.set(key, value)


def delete_values_from_redis_db(redis_client, kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.delete(key)


@pytest.fixture(scope="module")
def redis_client():
    return redis.Redis(host=os.environ['PROXY_RESP_HOST'], port=os.environ['PROXY_RESP_PORT'])


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


def test_proxy_get_request_for_all_keys_in_db_finds_a_value(redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        assert redis_client.get(key) != ""
        

def test_proxy_get_request_for_all_keys_in_db_returns_a_non_empty_string(redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        value = redis_client.get(key)
        assert value != ""


def test_proxy_get_request_for_all_keys_returns_correct_values(redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        assert value == redis_client.get(key)


def test_proxy_get_request_for_keys_not_in_db_returns_key_not_found(keys_not_in_db):
    for key in keys_not_in_db:
        assert "" == redis_client.get(key)


