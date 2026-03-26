import os
import requests

# 秘密の箱から3つの鍵を読み込む
LINE_TOKEN = os.environ['LINE_TOKEN']
USER_ID = os.environ['USER_ID']
NEWS_API_KEY = os.environ['NEWS_API_KEY']

def send_news():
    # 1. ニュースを取得（キーワード：株価, 経済）
    news_url = f'https://newsapi.org/v2/everything?q=株価 OR 経済&language=jp&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    articles = requests.get(news_url).json().get('articles', [])[:3] # 最新3件
    
    if not articles:
        return

    # 2. メッセージを組み立てる
    msg = "📢 本日の経済ニュースをお届けします！\n\n"
    for art in articles:
        msg += f"🔹 {art['title']}\n{art['url']}\n\n"

    # 3. あなたのLINEに送信する
    line_url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_TOKEN}'
    }
    body = {
        'to': USER_ID,
        'messages': [{'type': 'text', 'text': msg}]
    }
    
    res = requests.post(line_url, headers=headers, json=body)
    print("送信結果:", res.status_code)

if __name__ == "__main__":
    send_news()
