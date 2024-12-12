#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
# 基本的には
# - 入力と応答の対応リスト(argv[1])
# - 話者認識結果ID (argv[2])
# - 音声認識結果 (argv[3])
# を受け取って応答文および音声を生成する
#
# 前の応答への依存性を持たせたい場合は引数を追加すれば良い
import sys, os
import subprocess
import re

jtalkbin = 'open_jtalk '
#options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
options = '-m ../Voice/mei/mei_angry.htsvoice -ow ./tmp_out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic -r 1.5 -fm 1.0'


# 音声合成のコマンドを生成 (open jtalk を 使う場合)
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q ./tmp_out.wav; rm ./tmp_out.wav;'
    return jtalk + play


def ask_number():
    # 1. 人数を聞く
    question = "会話に参加する人数は何人ですか？"
    os.system(mk_jtalk_command(question))

    # 2. 人数を認識する
    while True:
        recognize_number_path = "./introduction/recognize_number.sh"
        answer_path = "/tmp/dialogue/asrresult.txt"
        result = subprocess.run(['bash', recognize_number_path], capture_output=True)
        
        asrresult = open(answer_path,'r')
        answer = asrresult.read().rstrip() # 人数がとってこれる
        asrresult.close()

        # 正規表現を使って数字を取り出す
        match = re.search(r'\d+', answer)

        if not match:
            not_found = "人数が認識されませんでした。もう一度、お答えください！"
            os.system(mk_jtalk_command(not_found + question))
            continue
 
        # 数字部分を整数に変換
        number = int(match.group())       
        ask_again = f"それでは、{str(number)}人でよろしいですね？変更はできません！"
        os.system(mk_jtalk_command(ask_again))
        
        # 確認をする
        recognize_number_path = "./introduction/recognize_number.sh"
        answer_path = "/tmp/dialogue/asrresult.txt"
        result = subprocess.run(['bash', recognize_number_path], capture_output=True)
        
        asrresult = open(answer_path,'r')
        answer = asrresult.read().rstrip() # 人数がとってこれる
        asrresult.close()
        
        if not answer == "はい":
            not_found = "申し訳ありませんでした。もう一度、お答えください！"
            os.system(mk_jtalk_command(not_found + question))
            continue
        
        # 確定できた！
        confirm = f"それでは、{str(number)}人で承りました！"
        os.system(mk_jtalk_command(confirm))
        return number

if __name__ == '__main__':
    number = ask_number()
    print(number)

