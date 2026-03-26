import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("USER_ID")

url = "https://api.line.me/v2/bot/message/push"

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": "テスト送信成功！🚀"
        }
    ]
}

res = requests.post(url, headers=headers, json=data)
print(res.status_code, res.text)
