#!/usr/bin/env python3
# coding: utf-8
#
# 自己紹介をさせつつ、録音を行う

import sys, os
import subprocess
import re

sys.path.append('..')
from dynamic_manager import dynamic_value_manager

jtalkbin = 'open_jtalk '
#options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
options = '-m ../Voice/mei/mei_angry.htsvoice -ow ./tmp_out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic -r 1.5 -fm 1.0'


# 音声合成のコマンドを生成 (open jtalk を 使う場合)
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q ./tmp_out.wav; rm ./tmp_out.wav;'
    return jtalk + play

def record(spk_num = 4):
    # 0. 音声ファイルリストを初期化
    spklist_path = "./introduction/train_data/wav-spklist.txt"
    if os.path.isfile(spklist_path):
        with open(spklist_path,"w") as f:
            pass

    # 1. 人数分の自己紹介を行う
    make_train_data_path = "./introduction/make_train_data.sh"
    for spk_id in range(1, spk_num+1):
        # チームメンバーの自己紹介を促す音声を流す
        dynamic_value_manager.set_value(f'【自己紹介】{str(spk_id)}番目の方、お願いします')
        os.system(mk_jtalk_command(f'{str(spk_id)}番目の人は、自己紹介をはじめてください。自己紹介が終わったら、少し間をおいてから、以上です、と言ってください。'))

        # 各メンバーの音声を保存
        res = subprocess.run(["bash", make_train_data_path,str(spk_id)], capture_output=True, text=True)

        # 次の人への自己紹介を促す
        os.system(mk_jtalk_command('ありがとうございました。'))
        if(spk_id<spk_num):
            os.system(mk_jtalk_command('次に、'))

    return 

if __name__ == '__main__':
    record()