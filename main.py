import os
import requests

# GitHubのSecretsからトークンを読み込みます
LINE_TOKEN = os.environ.get('LINE_TOKEN')

def get_my_id():
    if not LINE_TOKEN:
        print("エラー: GitHubのSecretsに 'LINE_TOKEN' が設定されていません。")
        return

    # LINEのサーバーにBotの情報を聞きに行きます
    url = 'https://api.line.me/v2/bot/info'
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    
    res = requests.get(url, headers=headers)
    
    print("\n" + "="*50)
    if res.status_code == 200:
        data = res.json()
        print(f"✅ 通信成功！ Botの名前は『{data.get('displayName')}』です。")
        print("\n【次のステップ】")
        print("1. スマホのLINEで、このBotに何か1文字メッセージを送ってください。")
        print("2. 送り終わったら、GitHubのActionsをもう一度実行してください。")
        print("3. すると、この下のログにあなたの『ユーザーID』が表示されるようになります。")
    else:
        print(f"❌ 通信エラー: {res.text}")
    print("="*50 + "\n")

if __name__ == "__main__":
    get_my_id()
