import os
import json
import requests

LINE_TOKEN = os.getenv("LINE_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
HEADERS = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

USER_FILE = "users.json"


# =========================
# ユーザー設定読み込み
# =========================
def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)


# =========================
# LINE送信
# =========================
def send_line(user_id, messages):
    data = {
        "to": user_id,
        "messages": messages
    }

    res = requests.post(LINE_PUSH_URL, headers=HEADERS, json=data)
    print(res.status_code, res.text)


# =========================
# ニュース取得
# =========================
def get_news(region=None, keyword=None):
    if keyword:
        url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={NEWS_API_KEY}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country={region or 'us'}&apiKey={NEWS_API_KEY}"

    res = requests.get(url)
    data = res.json()

    articles = data.get("articles", [])[:3]

    messages = []
    for a in articles:
        messages.append({
            "type": "text",
            "text": f"📰 {a['title']}\n{a['url']}"
        })

    return messages


# =========================
# Webhook（設定保存）
# =========================
def handle_webhook(event):
    users = load_users()

    user_id = event["source"]["userId"]

    if event["type"] == "postback":
        data = event["postback"]["data"]

        params = dict(x.split("=") for x in data.split("&"))
        type_ = params.get("type")
        value = params.get("value")

        if user_id not in users:
            users[user_id] = {}

        if type_ == "region":
            users[user_id]["region"] = value
            send_line(user_id, [{"type": "text", "text": f"地域を {value} に設定しました🌍"}])

        elif type_ == "ticker":
            users[user_id]["ticker"] = value
            send_line(user_id, [{"type": "text", "text": f"{value} のニュースを配信します📈"}])

        save_users(users)


# =========================
# 定期配信
# =========================
def run_batch():
    users = load_users()

    for user_id, setting in users.items():
        region = setting.get("region")
        ticker = setting.get("ticker")

        messages = get_news(region=region, keyword=ticker)
        send_line(user_id, messages)


# =========================
# 実行分岐
# =========================
if __name__ == "__main__":
    # GitHub Actions用
    run_batch()
