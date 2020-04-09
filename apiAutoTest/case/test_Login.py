import sys, os
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

from apiAutoTest.toolUtils.getData import getData
from apiAutoTest.api.baseApi import BusApi
from apiAutoTest.toolUtils.yamlUtils import Yaml
import time
import allure
import pytest


@allure.feature("Test login api")
class Test_Login():

    configFile = Yaml("./config/config.yaml").readYaml()
    tcFilepath = configFile["caseFile"]["path"].format(time.strftime("%Y-%m-%d"))
    sheetName = configFile["caseFile"]["loginSheet"].format(time.strftime("%Y-%m-%d"))
    getObj = getData(tcFilepath, sheetName)

    @pytest.mark.parametrize("id, desc, url, method, headers, payload, expected", getObj.data())
    def test_login(self, id, desc, url, method, headers, payload, expected):
        res = BusApi(id, desc, url, method, headers, payload, expected, "login")
        allure.attach("{0}".format(res.response()), "Response")
        res.assertion()

if __name__ == '__main__':
    pytest.main(["-s", "test_Login.py"])