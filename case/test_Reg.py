from toolUtils.getData import getData
from api.baseApi import BusApi
from toolUtils.yamlUtils import Yaml
import time
import pytest
import allure

@allure.feature("Test register api")
class TestRegister():

    tcFilepath = Yaml("./config/config.yaml").readYaml()["caseFile"]["path"].format(time.strftime("%Y-%m-%d"))
    sheetName = Yaml("./config/config.yaml").readYaml()["caseFile"]["registerSheet"].format(time.strftime("%Y-%m-%d"))
    getObj = getData(tcFilepath, sheetName)

    @pytest.mark.parametrize("id, desc, url, method, headers, payload, expected", getObj.data())
    def test(self, id, desc, url, method, headers, payload, expected):
        res = BusApi(id, desc, url, method, headers, payload, expected, "register")
        allure.attach("{0}".format(res.response()), "Response")
        res.assertion()