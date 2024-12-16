import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn import mixture
from matplotlib.colors import LogNorm

from get_mfcc import get_mfcc

# Irisデータセットの読み込み
iris = load_iris()
data = iris.data  # 特徴量データ
labels = iris.target  # ラベルデータ

print(data[:10])
print(labels[:10])

# ここをMFCCで持ってくる
data = []
labels = []

# 緊張データ
dir_path = "src/icebreak/get_emotion/data/tensed"


# 緊張していないデータ
mfcc, label = get_mfcc("new_vowels/test/spk1/spk1_aeiou_05.wav", 0)
data.extend(mfcc)
labels.extend(label)
mfcc, label = get_mfcc("new_vowels/test/spk2/spk2_aeiou_05.wav", 1)
data.extend(mfcc)
labels.extend(label)

# PCAによる次元削減
pca = PCA(n_components=2)
trans_pca = pca.fit_transform(data)

# プロット設定
fig, ax = plt.subplots()

cmap = plt.get_cmap("tab10")
color = [cmap(label) for label in labels]

ax.set_xlabel("PCA axis 1")
ax.set_ylabel("PCA axis 2")

# ラベルごとのデータをプロット
for i in range(2):
    ax.scatter(trans_pca[labels == i, 0], trans_pca[labels == i, 1], color=cmap(i), s=10, marker="o", label="Label: {}".format(i))
ax.legend()

# GMMの適用
gmm = mixture.GaussianMixture(n_components=2, covariance_type='full')
#gmm.fit(trans_pca)
gmm.fit(data)

# クラスタリング結果の予測
gmm_labels = gmm.predict(data)

# 予測結果の表示（例: 最初の10個のラベル）
print(gmm_labels[:100])
print(labels[:100])
# プロットを表示
x = np.linspace(-4, 4)
y = np.linspace(-2, 2)
X, Y = np.meshgrid(x, y)
XX = np.array([X.ravel(), Y.ravel()]).T
Z =  - gmm.score_samples(XX)
Z = Z.reshape(X.shape)

fig,ax=plt.subplots(dpi=150,figsize=(5,4))

ax.scatter(trans_pca[:, 0], trans_pca[:, 1], s=0.5,c=labels)
cont = ax.contourf(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=100.0), levels=np.logspace(-1, 3, 20), alpha=0.2, linestyles='dashed', linewidths=0.5)
ax.scatter(trans_pca[:, 0], trans_pca[:, 1], s=1, c=labels)

ax.set_title("GMMによるクラスタリングと等高線")
plt.show()