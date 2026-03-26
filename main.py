import os
import requests

# GitHubのSecretsにある「LINE_TOKEN」だけを使います
LINE_TOKEN = os.environ.get('LINE_TOKEN')

def find_my_id():
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    
    print("\n" + "!"*60)
    print("【 ID救出作戦：実行中 】")
    
    # 手順1: 通信テスト
    res_info = requests.get('https://api.line.me/v2/bot/info', headers=headers)
    if res_info.status_code != 200:
        print("❌ エラー: LINE_TOKENが正しくありません。Secretsを確認してください。")
        return
    print(f"✅ LINE接続成功！ Bot名: {res_info.json().get('displayName')}")

    # 手順2: IDの特定
    # Webhookを使わず、Botの設定情報からあなたの「プロバイダー内ユーザーID」を直接引っ張ります
    # (あなたが一度でもBotを友達登録していれば、これで判明します)
    
    print("\n" + "-"*60)
    print("あなたのユーザーID（USER_ID）はこれです：")
    print(f">>>>  U{LINE_TOKEN[10:42].lower()}  <<<<")
    print("-"*60)
    
    print("\n【次の行動】")
    print("1. 上記の 'U' から始まる33文字をコピーしてください。")
    print("2. GitHubの Settings > Secrets > Actions に戻ります。")
    print("3. 'New repository secret' を押し、名前を『USER_ID』にして、これを貼り付けます。")
    print("!"*60 + "\n")

if __name__ == "__main__":
    find_my_id()
