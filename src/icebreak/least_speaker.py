import pandas as pd

def least_speaker(filename, spk_num):
    # CSVを読み込む
    df = pd.read_csv(filename)

    # 話者ごとの発言秒数を集計
    speaker_duration = df.groupby("speaker_id")["duration"].sum()

    # 話者番号1からspk_numまでを対象に、発言時間が0の話者を追加
    all_speakers = set(range(1, spk_num + 1))
    existing_speakers = set(speaker_duration.index)

    missing_speakers = all_speakers - existing_speakers

    # 発言がない話者には0秒を割り当てる
    for missing in missing_speakers:
        speaker_duration[missing] = 0

    # 発言の総時間が最も少ない話者番号を取得
    least_talkative_speaker = speaker_duration.idxmin()

    return least_talkative_speaker
