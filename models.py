from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(500))
    image = db.Column(db.String(500))
    summary = db.Column(db.Text)  # ➕ Thêm dòng này
    content = db.Column(db.Text)
