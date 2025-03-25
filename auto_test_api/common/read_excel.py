import openpyxl


class CaseData:
    pass


class ReadExcel(object):

    def __init__(self, filename, sheet_name):
        self.filename = filename
        self.sheet_name = sheet_name

    def open(self):
        """打开工作簿，选择表单"""
        self.workbook = openpyxl.load_workbook(self.filename)
        self.sheet = self.workbook[self.sheet_name]

    def read_data(self):
        # 打开工作簿，选择表单
        self.open()
        # 按行获取所有格子对象
        rows = list(self.sheet.rows)
        # 获取第一个表头
        title = []
        for r in rows[0]:
            title.append(r.value)
        # 创建一个列表，用来存储所有的用例数据
        cases = []
        # 遍历除表头外所有行的数据
        for row in rows[1:]:
            # 创建一个列表，存放行的数据
            data = []
            # 遍历除每行的每列的数据
            for j in row:
                # 将格子数据添加到data列表中
                data.append(j.value)
            case = dict(zip(title, data))
            cases.append(case)
        self.close()
        return cases

    def read_data_obj(self):
        # 打开工作簿，选择表单
        self.open()
        # 按行获取所有格子对象
        rows = list(self.sheet.rows)
        # 获取第一个表头
        title = []
        for r in rows[0]:
            title.append(r.value)
        # 创建一个列表，用来存储所有的用例数据
        cases = []
        # 遍历除表头外所有行的数据
        for row in rows[1:]:
            # 创建一个列表，存放行的数据
            data = []
            # 遍历除每行的每列的数据
            for j in row:
                # 将格子数据添加到data列表中
                data.append(j.value)
                # 将表头和数据打包转换位列表
            case = list(zip(title, data))
            # 创建一个对象用来保存该行用例数据
            case_obj = CaseData()
            # 拆包遍历列表该行数据，使用setattr设置为对象的属性和属性值
            for k, v in case:
                setattr(case_obj, k, v)
                # 将对象添加到cases这个列表中
            cases.append(case_obj)
        self.close()
        # 返回cases（包含所有用例对象的列表）
        return cases

    def write_data(self, row, column, value):
        self.open()
        self.sheet.cell(row=row, column=column, value=value)
        self.workbook.save(self.filename)
        self.close()

    def close(self):
        """关闭工作簿"""
        self.workbook.close()



