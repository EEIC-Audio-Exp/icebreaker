import os
import subprocess
from introduction.ask_number import ask_number

def introduction():
    # 自己紹介のメイン処理
    # システムの説明音声を流す
    # -> 参加人数を尋ねる音声を流す
    # -> 参加人数を答える
    # -> 参加人数の音声から人数を取得
    spk_num = ask_number() #仮で4人に設定
    
    #音声ファイルリストを初期化
    spklist_path = "./introduction/train_data/wav-spklist.txt"
    if os.path.isfile(spklist_path):
        with open(spklist_path,"w") as f:
            pass
    
    make_train_data_path = "./introduction/make_train_data.sh"
    for spk_id in range(1, spk_num+1):
        # -> チームメンバーの自己紹介を促す音声を流す
        print(str(spk_id) + "人目の人は自己紹介をはじめてください。")
        # -> 各メンバーの音声を保存
        res = subprocess.run(["bash", make_train_data_path,str(spk_id)], capture_output=True, text=True)
        #print(res.stdout)
        #print(res.stderr)

    #全員の音声をもとに学習
    train_path = "../dialogue-demo/sid/train.sh"
    res = subprocess.run(["bash", train_path, spklist_path], capture_output=True, text=True)
    print(res.stdout)
    print(res.stderr)

    #自己紹介の終了
    print("これで自己紹介は終わりです。ありがとうございました。")
    pass

