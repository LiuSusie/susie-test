import xlrd
import xlwt
from xlutils.copy import copy

class ExcelOpration():

    #返回总的用例个数
    def count_rows(self,sheet):
        return  sheet.max_row-1

    #返回需要自动化执行的用例个数
    def auto_count_rows(self,sheet,column):

        # 指定要计数的特定数值
        value_to_count = 'yes'

        # 初始化计数器
        count = 0

        # 遍历列中的每个单元格
        for cell in sheet[column]:
            if cell.value == value_to_count:
                count += 1

        # print(f'\n数值 "{value_to_count}" 在列 {column} 中出现了 {count} 次。')
        return count

    def get_element_info(self,element,sheet,column):
        # 遍历列中的每个单元格
        for cell in sheet[column]:
            if cell.value == element:
                keyName=sheet.cell(row=cell.row,column=cell.column+1).value#获取关键字
                keyOpration = sheet.cell(row=cell.row, column=cell.column + 2).value #获取页面定位元素
                keyExpression = sheet.cell(row=cell.row, column=cell.column + 3).value  # 页面元素定位表达式
                return [keyName,keyOpration,keyExpression] #返回列表