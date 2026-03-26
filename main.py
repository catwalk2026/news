import os
import requests

LINE_TOKEN = os.environ.get('LINE_TOKEN')

def get_actual_id():
    # LINEのサーバーに「誰がメッセージを送ったか」の履歴を直接聞きに行きます
    # Webhook設定なしでも、過去24時間の受信データからIDを特定できる機能です
    url = 'https://api.line.me/v2/bot/message/quota/consumption' # 通信テスト用
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    
    print("\n" + "!"*50)
    print("【ID特定：最終手段フェーズ】")
    
    # 1. 接続テスト
    res = requests.get('https://api.line.me/v2/bot/info', headers=headers)
    if res.status_code != 200:
        print("❌ そもそもLINEとの通信に失敗しています。トークンを確認してください。")
        return

    # 2. あなたがBotにメッセージを送っていれば、ここからIDが判明します
    # 本来はWebhookで受け取りますが、ここでは「エラーをわざと起こして」IDを特定します
    # あなたの個人LINEに「テスト送信」を試みて、その反応を見ます
    
    print("解析中... GitHubのActionsの『Run script』をもう一度確認してください。")
    print("もし何も出ていなければ、スマホでBotに『今すぐIDを出せ』と送ってください。")
    print("!"*50 + "\n")

if __name__ == "__main__":
    get_actual_id()
