from flask import Flask, render_template, request, redirect, url_for
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
def home():
    query = request.args.get('q')
    if query:
        return redirect(url_for('data', q=query))
    else:
        return render_template('home.html')

@app.route('/data')
def data():
    keyword = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = 12

    if keyword:
        # Tìm kiếm theo từ khóa trong title, sau đó sắp xếp theo id giảm dần (mới nhất trước)
        filtered_articles = [a for a in Article.query.all() if keyword in a.title.lower()]
        articles = sorted(filtered_articles, key=lambda x: x.id, reverse=True)
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
@app.route('/data')
def view_data():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('data.html', articles=articles)

@app.route('/data-page')
def view_data():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('data.html', articles=articles)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
