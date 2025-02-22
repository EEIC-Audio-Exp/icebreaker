# icebreakシステムの骨組み

import threading
import time

from flask_site import app
from dynamic_manager import dynamic_value_manager
from icebreak.icebreak import icebreak
from introduction.introduction import introduction
from clear import clear


def main():
    """アイスブレイクシステム"""
    clear()
    time.sleep(3)
    
    
    # 自己紹介
    # システムの説明音声を流す
    # -> 参加人数を尋ねる音声を流す
    # -> 参加人数を答える
    # -> 参加人数の音声から人数を取得
    # -> チームメンバーの自己紹介を促す音声を流す
    # -> 各メンバーの音声を保存、学習させる
    spk_num = introduction()
    
    
    # アイスブレイク開始
    # 話題を提供 
    # -> メンバーが話す 
    # -> 音声から話者認識し、話した時間を測定 
    # -> ... 
    # -> 会話が止まった（1度目）：一定時間止まったら話している時間が短い人に会話を促す 
    # -> ... 
    # -> 会話が止まった（2度目）：次の話題を提供
    # -> ...
    # 指定された時間になったら終了
    icebreak(spk_num)



def run_app():
    global app
    app.run(debug=False)


if __name__ == "__main__":
    threading.Thread(target=run_app, daemon=True).start()
    main()
