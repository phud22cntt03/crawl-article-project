from flask import Flask, render_template, request
from models import db, Article
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vnexpress.db'
db.init_app(app)

# Các thể loại và slug
CATEGORIES = {
    'thoi-su': 'Thời sự',
    'the-gioi': 'Thế giới',
    'kinh-doanh': 'Kinh doanh',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao'
}

@app.route('/')
def index():
    keyword = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = 12

    if keyword:
        articles = Article.query.all()
        articles = [a for a in articles if keyword in a.title.lower()]
    else:
        articles = Article.query.order_by(Article.id.desc()).all()

    total = len(articles)
    start = (page - 1) * per_page
    paginated_articles = articles[start:start + per_page]
    total_pages = (total + per_page - 1) // per_page

    return render_template('index.html',
                           articles=paginated_articles,
                           current_time=datetime.now(),
                           current_page=page,
                           total_pages=total_pages,
                           keyword=keyword,
                           categories=CATEGORIES,
                           current_category=None)

@app.route('/category/<slug>')
def category_view(slug):
    category_name = CATEGORIES.get(slug)
    if not category_name:
        return "Không tìm thấy thể loại", 404

    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Article.query.filter(Article.category == category_name)
    articles = query.order_by(Article.id.desc()).all()

    total = len(articles)
    start = (page - 1) * per_page
    paginated_articles = articles[start:start + per_page]
    total_pages = (total + per_page - 1) // per_page

    return render_template('index.html',
                           articles=paginated_articles,
                           current_time=datetime.now(),
                           current_page=page,
                           total_pages=total_pages,
                           keyword=None,
                           categories=CATEGORIES,
                           current_category=slug)

@app.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
