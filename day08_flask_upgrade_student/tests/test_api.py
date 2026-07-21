# 这是一个示例 Python 脚本。


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
import unittest
from app import app
import sys
from pathlib import Path
# 获取项目根目录
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

# 下面保留你原本所有导入代码
from functools import wraps
from pathlib import Path
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from services.data_service import (
    load_category_api_data,
    load_dashboard_data,
    load_metric_api_data,
)
from services.qa_service import answer_question
from app import app
class FlaskApiTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    # 用例1：/health 接口返回200状态码
    def test_health_route(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)

    # 用例2：未登录访问 /api/metrics 被拦截
    def test_metrics_no_login(self):
        res = self.client.get("/api/metrics")
        self.assertNotEqual(res.status_code, 200)

    # 用例3：登录后访问指标接口，校验返回ok和metrics字段
    def test_metrics_login_success(self):
        # 模拟登录session，绕过登录拦截器
        with self.client.session_transaction() as sess:
            sess["username"] = "student"

        res = self.client.get("/api/metrics")
        data = res.get_json()
        self.assertEqual(data["ok"], True)
        self.assertIn("metrics", data)

    # 用例4：Fashion品类筛选接口校验筛选结果
    def test_category_filter_fashion(self):
        # 提前写入登录状态
        with self.client.session_transaction() as sess:
            sess["username"] = "student"

        res = self.client.get("/api/categories?category=Fashion")
        data = res.get_json()
        self.assertEqual(data["category"], "Fashion")
        self.assertGreater(len(data["rows"]), 0)

if __name__ == '__main__':
    unittest.main()