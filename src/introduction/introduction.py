from introduction.ask_number import ask_number
from introduction.record import record
from introduction.train import train

def introduction():
    # 自己紹介のメイン処理
    # システムの説明音声を流す
    # -> 参加人数を尋ねる音声を流す
    # -> 参加人数を答える
    # -> 参加人数の音声から人数を取得
    spk_num = ask_number() 
    
    # 順番に自己紹介
    # 自己紹介の音声を録音する
    record(spk_num)

    # 録音された音声を使って学習を行う
    train()

