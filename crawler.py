import requests
from bs4 import BeautifulSoup
from app import db, Article  # 👈 cần import từ app

def crawl_vnexpress():
    url = 'https://vnexpress.net'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for item in soup.select('.item-news'):
        title_tag = item.select_one('h3.title-news a')
        image_tag = item.select_one('img')
        
        if title_tag and image_tag:
            link = title_tag['href']
            title = title_tag.get_text(strip=True)
            image = image_tag.get('data-src') or image_tag.get('src')

            # Crawl nội dung bài viết
            content = crawl_article_content(link)
            summary = content[:150] + "..." if len(content) > 150 else content

            # ✅ Thêm vào DB
            article = Article(title=title, image=image, summary=summary, content=content)
            db.session.add(article)
            articles.append(article)

    db.session.commit()  # ✅ Ghi dữ liệu vào DB
    return articles

def crawl_article_content(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        paragraphs = soup.select('article.fck_detail p')
        content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        return content
    except:
        return ""
