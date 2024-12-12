#!/bin/bash
#
# 
# 

## dialogue directory ##
tmpdirname=../introduction/train_data

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

    #事後処理
    #現在は、10件保存したらループを抜けるようにしている

    #train_dataディレクトリ内に追加したデータを、リストにも追記
    echo -e "$filename\t$spkid" >> $tmpdirname/wav-spklist.txt
    if [ "$file_num" -eq 10 ];then
        break
    fi
    file_num=$((file_num + 1))

done
