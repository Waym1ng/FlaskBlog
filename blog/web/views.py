
from flask import Blueprint, render_template, url_for, request, redirect

from back.models import Article, Category

blue2 = Blueprint('web',__name__)


@blue2.route('/')
def re():

     return redirect(url_for('web.index',page=1))


@blue2.route('/index/page/<int:page>')
def index(page):
     # page = int(request.args.get('page'))
     articles = Article.query.order_by(Article.a_id.desc()).offset((page-1)*4).limit(4).all()
     categories = Category.query.filter().all()
     return render_template('web/index.html',articles=articles,categories=categories,page=page)


@blue2.route('/article/')
def article():

    categories = Category.query.filter().all()
    #获取文章的ID
    id = request.args.get('id')
    article = Article.query.filter(Article.a_id == id ).first()

    return render_template('web/article.html',article=article,categories=categories)


@blue2.route('/category/')
def category():
    #获取栏目的ID
    id = int(request.args.get('id'))
    categories = Category.query.filter().all()
    #用ID来获取某个栏目下的文章
    # category = categories[0] 这是一个Article对象
    # print(category.arts)
    return render_template('web/category.html',categories=categories,id=id-1)


@blue2.route('/tags/')
def tags():
     return render_template('web/tags.html')


@blue2.route('/links/')
def links():
     return render_template('web/links.html')


@blue2.route('/readers/')
def readers():
     return render_template('web/readers.html')












