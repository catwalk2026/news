import os
import requests

# 秘密の箱(Secrets)から3つの情報を読み込む
LINE_TOKEN = os.environ['LINE_TOKEN']
USER_ID = os.environ['USER_ID']
NEWS_API_KEY = os.environ['NEWS_API_KEY']

def send_news():
    # 1. ニュースを取得（日本のトップニュース）
    news_url = f'https://newsapi.org/v2/top-headlines?country=jp&apiKey={NEWS_API_KEY}'
    res = requests.get(news_url).json()
    articles = res.get('articles', [])[:3] # 最新3件
    
    if not articles:
        print("ニュースが見つかりませんでした")
        return

    # 2. メッセージを作成
    msg = "📢 お待たせしました！本日のニュースです\n"
    for art in articles:
        msg += f"\n🔹 {art['title']}\n{art['url']}\n"

    # 3. あなたのLINEに送信
    line_url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_TOKEN}'
    }
    body = {
        'to': USER_ID,
        'messages': [{'type': 'text', 'text': msg}]
    }
    
    response = requests.post(line_url, headers=headers, json=body)
    print("送信結果:", response.status_code)

if __name__ == "__main__":
    send_news()
