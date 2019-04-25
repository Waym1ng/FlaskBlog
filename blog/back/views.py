
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import db, User, Article, Category
from utils.functions import is_login

blue = Blueprint('back',__name__)

@blue.route('/',methods=['GET','POST'])
@is_login
def hello():
    return redirect(url_for('back.index'))


@blue.route('/index/',methods=['GET','POST'])
@is_login
def index():

    articles = Article.query.filter().all()
    count = len(articles)
    return render_template('back/index.html',count=count)


@blue.route('/article/',methods=['GET','POST'])
@is_login
def article():

    if request.method == 'GET':
        # page = request.args.get('page')
        #
        # articles = Article.query.filter().offset((int(page)-1)*5).limit(5).all()
        articles = Article.query.filter().limit(5).all()
        art = Article.query.filter().all()
        count = len(art)

        return render_template('back/article.html',articles=articles,count=count)

    if request.method == "POST":

        articles = Article.query.filter().all()

        data = []
        for article in articles:
            Dict = {}
            Dict['id'] = article.a_id
            Dict['title'] = article.title
            Dict['category'] = article.category.c_name
            create_time = article.create_time.strftime("%Y-%m-%d %X")
            Dict['create_time'] = create_time
            data.append(Dict)

        return jsonify({'code':200,'data':data})


@blue.route('/add-article/',methods=['GET','POST'])
@is_login
def add_article():
    if request.method == 'GET':
        return render_template('back/add-article.html')
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('describe')
        content = request.form.get('content')
        type = request.form.get('category')
        article = Article()
        article.title = title
        article.desc = desc
        article.content = content
        article.type = type
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('back.article',page=1))


@blue.route('/delete-article/',methods=['GET'])
@is_login
def delete_article():

    if request.method == 'GET':

        title = request.args.get('title')
        article = Article.query.filter(Article.title==title).first()

        db.session.delete(article)
        db.session.commit()

        return jsonify({'status':200})


@blue.route('/update-article/',methods=['GET','POST'])
@is_login
def update_article():


    if request.method == 'GET':
        id = request.args.get('id')
        article = Article.query.filter(Article.a_id == id).first()
        categories = Category.query.filter().all()

        return render_template('back/update-article.html',article=article,categories=categories)

    if request.method == 'POST':

        title = request.form.get('title')
        desc = request.form.get('describe')
        content = request.form.get('content')
        type = request.form.get('category')
        id = request.form.get('submit')
        article = Article.query.filter(Article.a_id == id).first()
        article.title = title
        article.desc = desc
        article.content = content
        article.type = type
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('back.article'))


@blue.route('/category/',methods=['GET','POST'])
@is_login
def category():
    if request.method == 'GET':

        categories = Category.query.filter().all()

        return render_template('back/category.html',categories=categories)

    if request.method == 'POST':

        name = request.form.get('name')
        alias = request.form.get('alias')

        category = Category()
        category.c_name = name
        category.alias = alias

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('back.category'))


@blue.route('/delete-category/<id>',methods=['GET'])
@is_login
def delete_category(id):

    if request.method == 'GET':

        category = Category.query.filter(Category.c_id==id).first()

        db.session.delete(category)
        db.session.commit()

        return redirect(url_for('back.category'))


@blue.route('/update-category/',methods=['GET','POST'])
@is_login
def update_category():

    if request.method == 'GET':
        id = request.args.get('id')

        category = Category.query.filter(Category.c_id == id).first()

        return render_template('back/update-category.html',category=category)

    if request.method == 'POST':

        name = request.form.get('name')
        alias = request.form.get('alias')
        id = request.form.get('submit')
        category = Category.query.filter(Category.c_id == id).first()
        category.c_name = name
        category.alias = alias

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('back.category'))



@blue.route('/login/',methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method =='POST':

        username = request.form.get('username')
        pwd = request.form.get('pwd')
        if username and pwd:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '账号不存在，请查证后再试'
                return render_template('back/login.html',error=error)
            if not check_password_hash(user.pwd,pwd):
                error = '密码错误，请查证后再试'
                return render_template('back/login.html',error=error)

            session['user_id'] = user.user_id
            return redirect(url_for('back.index'))
        else:
            error = '请输入完整的登陆信息'
            return render_template('back/login.html', error=error)


@blue.route('/register/',methods=['GET','POST'])
def register():

    if request.method == 'GET':
        return render_template('back/register.html')

    if request.method == 'POST':
        #获取数据
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        if username and pwd:
            user = User.query.filter(User.username ==username).first()
            if user:
                error = '该账号已被注册，请重新输入'
            else:
                user = User()
                user.username = username
                user.pwd = generate_password_hash(pwd)
                user.save()
                return redirect(url_for('back.login'))
        else:
            error = '账号或密码未填写'
            return render_template('back/register.html')


@blue.route('/logout/',methods=['GET'])
@is_login
def logout():

    del session['user_id']
    return redirect(url_for('back.login'))


@blue.route('/create_db/')
def create_db():
    db.create_all()
    return '创建表成功'