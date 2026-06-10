# OpenCSG 自动化测试项目

这是基于 OpenCSG 相关项目的自动化测试工程，包含 API 接口自动化测试与 UI 端自动化测试两部分，采用 Python + Pytest 技术栈实现，可直接运行并生成 Allure 测试报告。

---
## 项目结构
```
csg-automation-test/
├── .venv/ # Python 虚拟环境（依赖隔离）
├── commons/ # 公共工具模块
│ ├── init.py
│ ├── excelOpration.py # Excel 测试用例读取 / 写入工具
│ └── oprationElement.py # UI 元素操作封装（定位、等待、点击等）
├── driver/
│ └── chromedriver.exe # Chrome 浏览器驱动（与本地浏览器版本匹配）
├── reports/ # 测试报告与日志目录
│ ├── allure-api-report/ # API 测试 HTML 报告生成目录
│ ├── allure-api-result/ # API 测试结果数据（供 Allure 解析）
│ ├── allure-ui-report/ # UI 测试 HTML 报告生成目录
│ ├── allure-ui-result/ # UI 测试结果数据（供 Allure 解析）
│ ├── results.xml # JUnit 格式测试结果文件
│ └── test.log # 测试运行日志
├── testdata/ # 测试数据与配置目录
│ ├── init.py
│ ├── global_value.py # 全局变量 / 服务地址配置
│ ├── api_test_cases.xls # API 接口测试用例（数据驱动）
│ └── ui_test_cases.xlsx # UI 场景测试用例（数据驱动）
├── pytest.ini # Pytest 全局配置文件
├── README.md # 项目说明文档（当前文件）
├── test_api.py # API 自动化测试用例集
└── test_ui.py # UI 自动化测试用例集
```
## 模块说明

| 模块/文件 | 核心作用 |
| :--- | :--- |
| `commons/` | 封装通用工具，如 Excel 操作、UI 元素操作，实现用例与工具解耦 |
| `test_api.py` | 接口自动化用例集，基于 `requests` 实现，支持参数化与数据驱动 |
| `test_ui.py` | UI 自动化用例集，基于 `Selenium` 实现，覆盖页面交互与校验 |
| `reports/` | 存储测试报告与日志，支持 `Allure` 可视化报告生成 |
| `testdata/` | 维护测试用例与全局配置，便于批量修改与扩展 |
---

## 技术栈
- 语言：Python 3.x
- 测试框架：Pytest（参数化、Fixture、标记）
- API 测试：Requests + JSONPath
- UI 测试：Selenium
- 数据驱动：Excel 管理测试用例
- 报告工具：Allure Report
- 环境管理：venv 虚拟环境

---

## 环境搭建
1.  克隆项目到本地
    ```bash
    git clone https://github.com/你的用户名/你的仓库名.git
    cd csg-automation-test
2.创建并激活虚拟环境
python -m venv .venv

.\.venv\Scripts\activate

3.安装依赖

pip install -r requirements.txt
# 核心依赖（若没有 requirements.txt，可手动安装）
pip install pytest requests selenium allure-pytest openpyxl jsonpath-python


运行测试
1. API 自动化测试

# 运行 API 测试用例，生成 Allure 结果
pytest test_api.py --alluredir=reports/allure-api-result

# 生成并打开 HTML 报告
allure serve reports/allure-api-result
2. UI 自动化测试
# 运行 UI 测试用例，生成 Allure 结果
pytest test_ui.py --alluredir=reports/allure-ui-result

# 生成并打开 HTML 报告
allure serve reports/allure-ui-result

测试用例说明
API 自动化测试
用例管理：通过 api_test_cases.xls 实现数据驱动，支持用例批量维护
断言方式：状态码校验、响应体结构校验、关键字段断言
UI 自动化测试
元素操作：封装了常用的元素定位、等待、点击、输入等方法
用例管理：通过 ui_test_cases.xlsx 维护测试步骤与预期结果
扩展说明
项目已预留扩展接口，可直接新增用例到 Excel 中，无需修改核心代码
报告中会记录每个用例的执行结果、耗时与错误详情，便于定位问题