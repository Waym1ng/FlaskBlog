
# 使用装饰器去实现登录校验的功能
# @login_required
# 外层函数嵌套内层函数
# 外层函数返回内层函数
# 内层函数调用外层函数的参数
from functools import wraps

from flask import session, render_template, redirect, url_for, request

from back.models import User


def is_login(func):
    @wraps(func)
    def check():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('back.login'))
        # 查询出user_id 为登陆用户的信息
        user = User.query.filter(User.user_id == user_id).first()
        # 动态绑定在request上
        request.user = user

        return func()

    return check