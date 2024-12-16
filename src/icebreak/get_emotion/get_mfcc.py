import librosa

def get_mfcc(wav_path: str, label: int):
    y, sr = librosa.load(wav_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=18) # sampling rate
    return mfcc.T, [label for _ in range(len(mfcc[0]))]

if __name__ == "__main__":
    mfcc, label = get_mfcc("new_vowels/test/spk1/spk1_aeiou_05.wav", "label")
    print(mfcc.shape, label.shape)