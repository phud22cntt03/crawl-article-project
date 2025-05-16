import requests
from bs4 import BeautifulSoup
from app import db, Article

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
            content = crawl_article_content(link)
            summary = content[:150] + "..." if len(content) > 150 else content

            # Lấy category từ URL
            category = extract_category_from_url(link)

            article = Article(
                title=title,
                link=link,
                image=image,
                summary=summary,
                content=content,
                category=category
            )
            db.session.add(article)
            articles.append(article)

    db.session.commit()
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

def extract_category_from_url(url):
    try:
        parts = url.split('/')
        category_slug = parts[3] if len(parts) > 3 else "khac"
        category_map = {
            'thoi-su': 'Thời sự',
            'the-gioi': 'Thế giới',
            'kinh-doanh': 'Kinh doanh',
            'giai-tri': 'Giải trí',
            'the-thao': 'Thể thao'
        }
        return category_map.get(category_slug, 'Khác')
    except:
        return "Khác"
