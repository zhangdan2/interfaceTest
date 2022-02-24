import xlrd
import os
pro_dir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
def get_xls(xls_name, sheet_name,):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(pro_dir, 'testFile','case', xls_name)
    # open xls file
    file = xlrd.open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls