from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vnexpress.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    image = db.Column(db.String(500))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)

@app.route('/')
def index():
    keyword = request.args.get('q', '').lower()
    articles = Article.query.all()
    if keyword:
        articles = [a for a in articles if keyword in a.title.lower()]
    print(f"Tìm thấy {len(articles)} bài viết")  # 👈 thêm dòng này
    return render_template('index.html', articles=articles, current_time=datetime.now())


@app.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
