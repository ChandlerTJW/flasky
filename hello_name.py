# -*- coding: utf-8 -*-
# 增强版，添加了动态路由 /user/<name>
# 测试需要手动在 url 中输入 /user/name

# 创建 flask 实例
# app是主模块的名字，通过传入__name__参数来指定
from flask import Flask, session, redirect, url_for, flash

app = Flask(__name__)
# 设置lask-WTF
app.config['SECRET_KEY'] = 'hard to guess string'
# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField("what is your name?", validators=[Required()])
    submit = SubmitField('Submit')


# flask 提供的render_template 函数把 jinja2 模板引擎集成到了程序中
from flask import render_template

# Flask-Bootstrap 初始化
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)

# Flask-Moment 初始化
from flask_moment import Moment

moment = Moment(app)

# 加入datetime变量
from datetime import datetime


# 用 app.route 装饰器把视图函数 index 注册为路由
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           current_time=datetime.utcnow())


# 自定义错误页面 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 自定义错误页面 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 通过在 url 中传入参数 name，把视图函数 user 注册为动态路由
# 第1个参数是模板的文件名，随后参数是键值对，表示模板中变量对应的真实值
# 左边的 name 是模板中使用的占位符，右边 name 是作用域中的变量
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# 确保只有在执行这个脚本时，才运行 web 服务器
# 并启用调试模式
if __name__ == '__main__':
    app.run(debug=True)
