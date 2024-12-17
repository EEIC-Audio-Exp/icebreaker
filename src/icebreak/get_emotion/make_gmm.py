import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.decomposition import PCA
from sklearn import mixture
from matplotlib.colors import LogNorm
from sklearn.metrics import accuracy_score
import joblib

import os

from get_mfcc import get_mfcc


# データのmfccを取得してモデルを作る

# 非緊張モデル
dir_path = "src/icebreak/get_emotion/data/relaxed"
data_relaxed = []
labels_relaxed = []
file_names = os.listdir(dir_path)
for file_name in file_names:
    mfcc, label = get_mfcc(os.path.join(dir_path, file_name), 0)
    data_relaxed.extend(mfcc)
    labels_relaxed.extend(label)

# GMMのモデルを作成
gmm_relaxed = mixture.GaussianMixture(n_components=32, covariance_type='full')
gmm_relaxed.fit(data_relaxed)
# モデルをファイルに保存
joblib.dump(gmm_relaxed, 'src/icebreak/get_emotion/models/gmm_relaxed_model.pkl')

# 緊張モデル
dir_path = "src/icebreak/get_emotion/data/tensed"
data_tensed = []
labels_tensed = []
file_names = os.listdir(dir_path)
for file_name in file_names:
    mfcc, label = get_mfcc(os.path.join(dir_path, file_name), 1)
    data_tensed.extend(mfcc)
    labels_tensed.extend(label)

# GMMのモデルを作成
gmm_tensed = mixture.GaussianMixture(n_components=32, covariance_type='full')
gmm_tensed.fit(data_tensed)
# モデルをファイルに保存
joblib.dump(gmm_tensed, 'src/icebreak/get_emotion/models/gmm_tensed_model.pkl')

# クラスタリング結果の予測
data = data_relaxed + data_tensed
labels = labels_relaxed + labels_tensed
gmm_relaxed_score = gmm_relaxed.score_samples(data)  # リラックス音声の対数尤度
gmm_tensed_score = gmm_tensed.score_samples(data)    # 緊張音声の対数尤度

# 最も尤度が大きいモデルを選択
predicted_labels = np.argmax(np.vstack([gmm_relaxed_score, gmm_tensed_score]), axis=0)

# クラスターの再マッピング
# 混同行列を作成
contingency_matrix = np.zeros((2, 2), dtype=int)  # クラス数が2の場合

for true_label, predicted_label in zip(labels, predicted_labels):
    contingency_matrix[true_label, predicted_label] += 1

print(contingency_matrix)  # 混同行列を表示して確認

# 正答率の計算
accuracy = accuracy_score(labels, predicted_labels)
print("正答率:", accuracy)