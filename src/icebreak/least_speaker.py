import pandas as pd

def least_speaker(filename):
    # CSVを読み込む
    df = pd.read_csv(filename)

    # 話者ごとの発言秒数を集計
    speaker_duration = df.groupby("speaker_id")["duration"].sum()

    # 発言の総時間が最も少ない話者番号を取得
    least_talkative_speaker = speaker_duration.idxmin()

    return least_talkative_speaker
