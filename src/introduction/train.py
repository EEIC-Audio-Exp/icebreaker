#!/usr/bin/env python3
# coding: utf-8
#
# 録音データをもとに学習を行う

import sys, os
import subprocess
import re
from multiprocessing import Process

sys.path.append('..')
from dynamic_manager import dynamic_value_manager

jtalkbin = 'open_jtalk '
#options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
options = '-m ../Voice/mei/mei_angry.htsvoice -ow ./tmp_out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic -r 1.0 -fm 1.0'


# 音声合成のコマンドを生成 (open jtalk を 使う場合)
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q ./tmp_out.wav; rm ./tmp_out.wav;'
    return jtalk + play

def task_train():
    train_path = "../dialogue-demo/sid/train.sh"
    spklist_path = "./introduction/train_data/wav-spklist.txt"
    res = subprocess.run(["bash", train_path, spklist_path], capture_output=True, text=True)

def task_jtalk():
    end_intro = "自己紹介が終わったので、ここからアイスブレイキングに入ります。私から話題を提示しますので、その話題についてみなさんで自由に話し合いましょう。"
    dynamic_value_manager.set_value('ここからアイスブレイキングに入ります')
    os.system(mk_jtalk_command(end_intro))

    end_intro2 = "システムの準備が終わるまで、少々お待ちください。"
    os.system(mk_jtalk_command(end_intro2))


def train():
    #全員の音声をもとに学習しつつ、その間を音声でもたせる
    process_train = Process(target=task_train)
    process_jtalk = Process(target=task_jtalk)

    process_train.start()
    process_jtalk.start()

    process_train.join()
    process_jtalk.join()
    
    print("話者認識用の学習が完了しました")
    return

if __name__ == '__main__':
    train()