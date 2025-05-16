from app import app, db
from crawler import crawl_vnexpress

with app.app_context():
    db.create_all()
    crawl_vnexpress()
    print("✅ Đã crawl và lưu bài viết.")
