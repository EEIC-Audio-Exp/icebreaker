import joblib
from get_mfcc import get_mfcc
import numpy as np

def get_tension(wav_path: str)->int:
    
    # モデルの読み込み
    gmm_relaxed = joblib.load('src/icebreak/get_emotion/models/gmm_relaxed_model.pkl')
    gmm_tensed = joblib.load('src/icebreak/get_emotion/models/gmm_tensed_model.pkl')

    # MFCCの取得
    mfcc, label = get_mfcc(wav_path, 1)

    # 尤度の計算
    gmm_relaxed_score = gmm_relaxed.score_samples(mfcc)  # リラックス音声の対数尤度
    gmm_tensed_score = gmm_tensed.score_samples(mfcc)    # 緊張音声の対数尤度

    min_score = min(np.min(gmm_relaxed_score), np.min(gmm_tensed_score))
    max_score = max(np.max(gmm_relaxed_score), np.max(gmm_tensed_score))

    gmm_relaxed_score = (gmm_relaxed_score - min_score) / (max_score - min_score)
    gmm_tensed_score = (gmm_tensed_score - min_score) / (max_score - min_score)

    score = np.mean(gmm_tensed_score) / (np.mean(gmm_relaxed_score) + np.mean(gmm_tensed_score))

    # 40未満なら0、60より大きければ100、40～60の間は線形にマッピング
    if score < 0.4:
        tension_score = 0
    elif score > 0.6:
        tension_score = 100
    else:
        tension_score = (score - 0.4) * 100 / (0.6 - 0.4)

    tension_score = int(tension_score)
    # print(tension_score)

    # 最も尤度が大きいモデルを選択
    predicted_labels = np.argmax(np.vstack([gmm_relaxed_score, gmm_tensed_score]), axis=0)
    # print(predicted_labels) # デバッグ用

    print(tension_score)
    return tension_score

if __name__ == "__main__":
    get_tension("src/icebreak/get_emotion/data/tensed/F2_fear_free_01.wav")
    get_tension("src/icebreak/get_emotion/data/relaxed/F2_happy_free_01.wav")
    get_tension("src/icebreak/get_emotion/data/tensed/M2_fear_free_01.wav")
    get_tension("src/icebreak/get_emotion/data/relaxed/M2_happy_free_01.wav")