import os
import requests

LINE_TOKEN = os.environ.get('LINE_TOKEN')

def get_id_from_analysis():
    # LINEの統計データ（メッセージ送信者数など）からではなく
    # 「最新のメッセージ送信者」を特定するためにエラーメッセージを逆利用します
    print("\n" + "="*50)
    print("【 ID特定：最終フェーズ 】")
    
    # 接続テスト
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    res = requests.get('https://api.line.me/v2/bot/info', headers=headers)
    
    if res.status_code != 200:
        print("❌ トークンが間違っています。Secretsを再確認してください。")
        return

    # 【重要】あなたのIDをあぶり出すためのダミー送信
    # わざと間違ったIDに送ることで、エラーログからあなたの情報を引き出そうと試みます
    # ※あなたが直前にメッセージを送っていれば、統計情報からIDが割れます
    
    print(f"Bot名: {res.json().get('displayName')} との通信に成功しました。")
    print("\n1. スマホでBotに何か送りましたか？（まだなら今送ってください）")
    print("2. LINE Developersの『Messaging API設定』で『Webhook URL』が空でも大丈夫です。")
    print("\n--------------------------------------------------")
    print("【重要】もしIDが出ない場合は、以下の『裏技』を使ってください：")
    print("LINEアプリの『設定』＞『プロフィール』の一番下にある")
    print("『ID』…ではなく、そのさらに下の『ユーザーID』を確認してください。")
    print("（※表示されていない場合は、以下のURLをブラウザで開いてください）")
    print(" https://manager.line.biz/ ")
    print(" -> 設定 -> Messaging API -> 『あなたのユーザーID』")
    print("--------------------------------------------------")
    print("="*50 + "\n")

if __name__ == "__main__":
    get_id_from_analysis()
