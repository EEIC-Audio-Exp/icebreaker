#!/usr/bin/env python3
# coding: utf-8
#
#
# 「以上です」かどうかを判定する
import sys, os

if __name__ == '__main__':
    # 認識結果
    asrresult = open(sys.argv[1],'r')
    endword = asrresult.read().rstrip()
    asrresult.close()

    #cmscore出力
    cmscore = open(sys.argv[2],'r')
    cmout = list(cmscore.read().split())
    cmscore.close()

    # 以上ですかどうかを判定
    if(endword == "以上です" and float(cmout[2]) > 0.9):
        print(1)
    else:
        print(0)

