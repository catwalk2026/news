import os
import requests

# 秘密の箱から3つの鍵を読み込む
LINE_TOKEN = os.environ['LINE_TOKEN']
USER_ID = os.environ['USER_ID']
NEWS_API_KEY = os.environ['NEWS_API_KEY']

def send_news():
    # 検索条件：特定の国を指定せず、世界中の「今」話題のニュース(Top Headlines)を取得
    # 言語も指定しないことで、海外のニュースも混ざるようになります
    news_url = f'https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}'
    
    try:
        res = requests.get(news_url).json()
        articles = res.get('articles', [])[:5] # 少し多めに5件に増やしました
        
        if not articles:
            # もし空なら、より広範囲に「World News」というキーワードで検索
            backup_url = f'https://newsapi.org/v2/everything?q=news&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
            res = requests.get(backup_url).json()
            articles = res.get('articles', [])[:5]

        if not articles:
            print("ニュースがどうしても見つかりませんでした")
            return

        msg = "🌍 【World News Express】 🌍\n"
        for art in articles:
            title = art.get('title', 'No Title')
            url = art.get('url', '')
            # 出典元（ロイターやBBCなど）があれば表示
            source = art.get('source', {}).get('name', 'Unknown')
            msg += f"\n📌 {title}\n(Source: {source})\n{url}\n"

        # LINEに送信
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

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    send_news()
