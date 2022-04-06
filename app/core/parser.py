import re


def parse_resp_get(resp):
    resp = resp.decode('utf-8')
    assert resp[:2] == '*2'
    resp = resp[2:]
    assert resp[:5] == '$3GET'
    resp = resp[5:]
    assert resp[:1] == '$'



# class RespParser:
#     def __init__(self):
#         self.delims = '\* |\$'
#
#     def parse(self, resp: bytearray):
#         resp = resp.decode('utf-8')
#
#         for i in len(resp):
#             c = resp[i]
#             resp = resp[1:]
#
#         split_resp = re.split(self.delims, resp)