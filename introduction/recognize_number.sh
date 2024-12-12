#! /bin/bash
# 音声をとってきて、何人参加するかをintで返す関数

## dialogue directory ##
tmpdirname=/tmp/dialogue

# もしディレクトリが存在しなければ作成
if [ ! -e $tmpdirname ];then
	mkdir ${tmpdirname}
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

	# # 数字を認識する
	# sidfile=${tmpdirname}/spkid.txt
	# #cd sid;
	# bash sid/test.sh $filename $sidfile;
	# #bash sid/test.sh record_ATR/wav/s4_b20.wav $sidfile
	# #cd ..
	
	# # 現在の話者番号を格納
	# # もし前の状態を保存しておきたければ別変数/別ファイルを用意する
	# sidnum=$(cat $sidfile)

	# # 音声認識
	asrresult=${tmpdirname}/asrresult.txt
	echo $filename > ${tmpdirname}/list.txt

	# # 音声認識をして結果をファイルに保存
	# # もし前の状態を保存しておきたければ別変数/別ファイルを用意する
	# julius -C introduction/asr/grammar.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult}julius -C introduction/asr/grammar.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g'
	julius -C introduction/asr/grammar.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult}
	rm ${tmpdirname}/list.txt

	echo $asrresult

	# # 事後処理
	# rm $filename $sidfile $asrresult
	exit;
done
# ここは実行されないはず
rmdir $tmpdirname
