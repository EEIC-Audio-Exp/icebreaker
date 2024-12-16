#!/bin/bash
#
# 
# 

## dialogue directory ##
tmpdirname=./introduction/train_data

#話者番号
spkid=$1

#ファイル番号
file_num=1

# もしディレクトリが存在しなければ作成
if [ ! -e $tmpdirname ];then
	mkdir ${tmpdirname}
fi
if [ ! -e $tmpdirname/wav ];then
	mkdir ${tmpdirname}/wav
fi

while true; do
	# adinrec による録音
	filename=${tmpdirname}/wav/s${spkid}_$(printf "%03d" $file_num).wav
	padsp adinrec $filename > /dev/null
	# Ctrl-C で抜けるための処理
	if [ ! -e $filename ];then
		rmdir $tmpdirname
		exit;
	fi

	# # 音声認識
	asrresult=${tmpdirname}/asrresult.txt
	echo $filename > ${tmpdirname}/list.txt
	cmscore=${tmpdirname}/cmscore.txt


	# # 音声認識をして結果をファイルに保存
	# # もし前の状態を保存しておきたければ別変数/別ファイルを用意する
	julius -C introduction/asr/grammar_end_intro.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult}
	julius -C introduction/asr/grammar_end_intro.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^cmscore1: " > ${cmscore}

	# 音声認識結果を処理してもらう
	# 「以上です」と判定できたら1, そうでなければ0を返す
	is_endword=$(./introduction/check_endword.py $asrresult $cmscore)

    #事後処理
    #現在は、10件保存したらループを抜けるようにしている

    #train_dataディレクトリ内に追加したデータを、リストにも追記
    echo -e "$filename\t$spkid" >> $tmpdirname/wav-spklist.txt
    if [ "$is_endword" -eq 1 ];then
        break
    fi
    file_num=$((file_num + 1))

	rm $asrresult $cmscore


done
