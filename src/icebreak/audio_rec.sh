#!/bin/bash
#
# 音声対話システムデモ（bash 版）
# 

## dialogue directory ##
tmpdirname=./input

# もしディレクトリが存在しなければ作成
if [ ! -e $tmpdirname ];then
	mkdir ${tmpdirname}
fi

# 現在のタイムスタンプを取得
timestamp=$(date +"%Y%m%d_%H%M%S")

# 録音ファイル名にタイムスタンプを付与
filename=${tmpdirname}/input_${timestamp}.wav

# 録音開始を監視するためのタイムアウト時間（5秒）
timeout=5
start_time=$(date +%s)
    
# adinrec による録音
# filename=${tmpdirname}/input.wav
padsp adinrec $filename > /dev/null &


# 録音プロセスのPIDを取得
pid=$!

# タイムアウトの間、録音が開始されたかを監視
while true; do
    # 録音プロセスがまだ実行中か確認
    if ps -p $pid > /dev/null; then
        # 録音が開始された場合、5秒以内に終了した場合の処理
        if [ -e $filename ]; then
            echo $filename  # 録音ファイル名を標準出力
            exit 0  # 正常終了
        fi
    else
        # 録音が終了した場合（異常終了等）
        exit 1
    fi

    # 5秒経過した場合、録音が開始されなかったことを示す
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ $elapsed_time -ge $timeout ]; then
        echo "Recording did not start within $timeout seconds."  # タイムアウトメッセージ
        exit 2  # タイムアウト終了
    fi

    # 少し待機してから再チェック
    sleep 0.5
done


	# # Ctrl-C で抜けるための処理
	# if [ ! -e $filename ];then
	# 	# rmdir $tmpdirname
	# 	exit;
	# fi

    # # # ファイル名を標準出力
    # echo $filename
