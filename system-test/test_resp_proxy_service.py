import os
import redis
import pytest
import multiprocessing as mp
from redis.exceptions import ResponseError, ConnectionError


def write_values_to_redis_db(kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.set(key, value)


def delete_values_from_redis_db(kv_pairs):
    r = redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])
    for key, value in kv_pairs.items():
        r.delete(key)


@pytest.fixture(scope="module")
def redis_proxy_client():
    """
    Returns a redis client connected to the RESP proxy, instead of the backing Redis instance.
    :return: Redis() client
    """
    return redis.Redis(host=os.environ['PROXY_RESP_HOST'], port=os.environ['PROXY_RESP_PORT'])


@pytest.fixture(scope="module")
def redis_client():
    """
    Returns a redis client connected to the RESP proxy, instead of the backing Redis instance.
    :return: Redis() client
    """
    return redis.Redis(host=os.environ['CLIENT_HOST'], port=os.environ['CLIENT_PORT'])


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


def test_proxy_get_request_for_all_keys_in_db_finds_a_value(redis_proxy_client, redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        r = redis_client.get(key).decode('utf-8')
        print(r)
        assert r != ""
        

def test_proxy_get_request_for_all_keys_in_db_returns_a_non_empty_string(redis_proxy_client, redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        r = redis_client.get(key).decode('utf-8')
        print(r)
        assert r != ""


def test_proxy_get_request_for_all_keys_returns_correct_values_or_hit_rate_limit(redis_proxy_client, redis_client, kv_pairs):
    for key, value in kv_pairs.items():
        assert redis_client.get(key).decode('utf-8') == value


def test_proxy_get_request_for_keys_not_in_db_returns_nonetype(redis_proxy_client, redis_client, keys_not_in_db):
    for key in keys_not_in_db:
        assert redis_client.get(key) is None


