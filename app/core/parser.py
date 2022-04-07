import logging


def parse_resp_get_for_key(resp):
    """
    Parse a GET request and return the corresponding response.

    Expected format:
    *2$3\r\nGET\r\n<key>\r\n
    *2\r\n$3\r\nGET\r\n$4\r\nkey1\r\n

    :param resp:
    :return:
    """
    resp = resp.decode('utf-8')
    resp = resp.split('\r\n')
    assert resp[:3] == ["*2", "$3", "GET"]
    return resp[-2]


def encode_resp_get_response(value: str) -> bytes:
    sz = len(value)
    if sz == 0:
        return f"${-1}\r\n".encode('utf-8')
    return f"${sz}\r\n{value}\r\n".encode('utf-8')
