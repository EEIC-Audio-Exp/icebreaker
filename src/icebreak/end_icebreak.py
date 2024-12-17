import os
from .speak import mk_jtalk_command

def end_icebreak():
    speak_str = f"これで、アイスブレイクを終了します。お疲れ様でした。"
    os.system(mk_jtalk_command(speak_str))

