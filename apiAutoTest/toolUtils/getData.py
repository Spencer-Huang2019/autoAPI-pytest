from apiAutoTest.toolUtils.excelUtils import excelRead

class getData(object):
    def __init__(self, filepath, sheetName):
        self.filepath = filepath
        self.sheetName = sheetName

    def data(self):
        excel = excelRead(self.filepath)
        workbook = excel.open()
        sheetInfo = excel.getSheetInfo(self.sheetName, 0, 7)

        return sheetInfo

if __name__ == '__main__':
    filepath = "..\..\documents\\api_TC_result.xls"
    getObj = getData(filepath, "login")
    print(list(getObj.data()))
    print(getObj.data())