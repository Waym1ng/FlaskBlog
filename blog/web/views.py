
from flask import Blueprint, render_template, url_for,request

from back.models import Article, Category

blue2 = Blueprint('web',__name__)


@blue2.route('/')
def index():

     articles = Article.query.filter().all()
     categories = Category.query.filter().all()

     return render_template('web/index.html',articles=articles,categories=categories)


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
    id = request.args.get('id')
    categories = Category.query.filter().all()
    #用ID来获取某个栏目下的文章
    # category = categories[0]
    # print(category.arts)
    return render_template('web/category.html',categories=categories,id=int(id)-1)


@blue2.route('/tags/')
def tags():
     return render_template('web/tags.html')


@blue2.route('/links/')
def links():
     return render_template('web/links.html')


@blue2.route('/readers/')
def readers():
     return render_template('web/readers.html')












