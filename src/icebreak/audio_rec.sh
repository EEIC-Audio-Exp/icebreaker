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

# スクリプトのディレクトリを取得
script_dir=$(cd $(dirname $0); pwd)

# データをCSVファイルに保存
output_csv="$script_dir/data.csv"  # Voiceディレクトリを基準に保存先を指定
output_dir=$(dirname $output_csv)
if [ ! -d $output_dir ]; then
    mkdir -p $output_dir
fi

# CSVのヘッダーを初回作成
if [ ! -e $output_csv ]; then
    echo "speaker_id,transcribe_result,duration" > $output_csv
fi

while true; do
	# adinrec による録音
	filename=${tmpdirname}/input.wav
	padsp adinrec $filename > /dev/null
	# Ctrl-C で抜けるための処理
	if [ ! -e $filename ];then
		rmdir $tmpdirname
		exit;
	fi

	# 話者認識
	sidfile=../../dialogue-demo/sid/spkid.txt
	#cd sid;
	bash ../../dialogue-demo/sid/test.sh $filename $sidfile;
	#bash sid/test.sh record_ATR/wav/s4_b20.wav $sidfile
	#cd ..
	
	# 現在の話者番号を格納
	# もし前の状態を保存しておきたければ別変数/別ファイルを用意する
	sidnum=$(cat $sidfile)

    # WAVファイルの情報を取得
    duration=$(soxi -D "$filename")  # 秒数

	# transcribe.pyによる文字起こし
    transcribe_result=$(python3 transcribe.py "$filename")

    # データをCSVに保存
    echo "$sidnum,\"$transcribe_result\",$duration" >> $output_csv
    echo "Saved to CSV: $sidnum,\"$transcribe_result\",$duration"

	# 事後処理
	rm $filename $sidfile $asrresult
done
# ここは実行されないはず
rmdir $tmpdirname