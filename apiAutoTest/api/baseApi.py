import os
from os import path
import sys

d = path.dirname(__file__)
parent_path = os.path.dirname(d)
sys.path.append(parent_path)

from apiAutoTest.toolUtils.logUtils import log
import json
import requests
import time
from apiAutoTest.toolUtils.yamlUtils import Yaml

class Api(object):
    def __init__(self, url, method, headers, payload, logApi):
        self.url = url
        self.method = method
        self.headers = headers
        self.payload = payload
        self.logfile = Yaml("./config/config.yaml").readYaml()["logFile"][logApi].format(time.strftime("%Y-%m-%d"))

    def logger(self):
        return log(self.logfile)

    def request(self):
        logger = self.logger()
        res = None
        # logger.msg("[url:%s headers:%s payload:%s]" % (self.url,self.headers,self.payload),"info")
        if self.headers:
            headers = json.loads(self.headers)
        else:
            headers = None

        if self.payload:
            payload = json.dumps(json.loads(self.payload))
        else:
            payload = None

        if self.method.upper() == "POST":
            try:
                res = requests.post(self.url, headers=headers, data=payload)
            except Exception:
                logger.msg("Request url:{} FAIL!!!".format(self.url), "error")
            else:
                logger.msg("Request url:{} SUCCESS!".format(self.url), "info")

        if self.method.upper() == "GET":
            try:
                res = requests.get(self.url, headers=headers, params=payload)
            except Exception:
                logger.msg("Request url:{} FAIL!!!".format(self.url), "error")
            else:
                logger.msg("Request url:{} SUCCESS!".format(self.url), "info")
        return res

class BusApi(Api):

    def __init__(self, id, desc, url, method, headers, payload, expected, logApi):
        super().__init__(url, method, headers, payload, logApi)
        self.id = id
        self.desc = desc
        self.expected = expected
        self.res = self.request()

    def response(self):
        return self.res.json()

    def assertion(self):
        logger = self.logger()
        expected_payload = json.loads(self.expected)
        statusCode = self.res.status_code

        if statusCode == 200:
            res_payload = self.res.json()
            logger.msg("TC%d %s: statusCode: %d resBody:%s" % (self.id,self.desc,statusCode,res_payload), "info")
            for item in expected_payload.keys():
                assert (res_payload[item] == expected_payload[item])
        else:
            logger.msg("TC%d %s: statusCode: %d FAIL!!!" % (self.id, self.desc, statusCode), "info")