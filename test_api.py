import os
import pytest
from xToolkit import xfile
import requests
import jsonpath
from testdata.global_value import  g_var
from string import Template
import allure
from pathlib import Path


# 接口的测试用例保存在api_test_cases.xls，首先读取测试用例
# 当前脚本所在目录（就是项目根目录）
current_dir = Path(__file__).parent
# 拼接 Excel 文件路径
excel_path = current_dir / "testdata" / "api_test_cases.xls"
# 读取目标Excel表格，并将其转化为列表
case_list = xfile.read(str(excel_path)).excel_to_dict(sheet=0)
# print(case_list)
# print("--------------")

class TestApiCases:
    # pytest参数化，自动循环执行
    @pytest.mark.parametrize("case_dict", case_list)
    def test_excel_case_(self,case_dict):

        # 初始化/修改url值，通过存贮对象
        url = case_dict.get("接口URL")
        dict = g_var().show_dict()
        url_ = Template(url).substitute(dict)
        #print(f'url_={url_}')

        res = requests.request(url=url_,
                               method=case_dict.get("请求方式"),
                               params=case_dict.get("URL参数"),  # 字典/字节序列，作为参数增加到URL中
                               data=case_dict.get("json参数")  # 字典/字节序列/文件对象，作为request的内容
                               )

        # 修改dict/填入dict值，数据来源是提取参数(上个接口返回的token),提取参数来源就是case_dict
        mm=case_dict.get("提取参数")
        print('提取参数='+mm)

        if mm != '':
            try:
                list_ = jsonpath.jsonpath(res.json(), '$..' + mm)  # ['token值']
                g = g_var()
                g.set_dict(mm, list_[0])
                g.get_dict_value(mm)
            except Exception as e:
                print(f"无法提取 {mm}，错误：{e}")

        #判断返回状态码是否正确
        assert res.status_code == case_dict.get("预期状态码")

        #判断预期返回字段名对应的值与预期返回字段值一致（或包含）
        if case_dict.get("预期返回字段值")!= '':

            exp_zd1=jsonpath.jsonpath(res.json(), '$..' + case_dict.get("预期返回字段名"))
            exp_zdz1 = case_dict.get("预期返回字段值")
            assert str(exp_zdz1)  in str(exp_zd1)


if __name__ == '__main__':

    pytest.main(['-vs', "./test_api.py", "--alluredir", "./reports/allure-api-result"])
    os.system(r"allure generate --clean ./reports/allure-api-result -o ./reports/allure-api-report")