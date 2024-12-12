import os
from speak import mk_jtalk_command

def prompt_quiet_speaker(speaker_id: int):
    speak_str = f"では、{speaker_id}番さん、あなたはどうでしょうか？"
    os.system(mk_jtalk_command(speak_str))


if __name__ == '__main__':
    for i in range(1, 6):
        prompt_quiet_speaker(i)
