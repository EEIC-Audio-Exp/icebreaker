import librosa

def get_mfcc(wav_path: str, label: int):
    # Load the audio file
    y, sr = librosa.load(wav_path)
    
    # Trim silence
    y_trimmed, _ = librosa.effects.trim(y, top_db=30)

    # Compute MFCC
    mfcc = librosa.feature.mfcc(y=y_trimmed, sr=sr, n_mfcc=18)  # Sampling rate
    
    # Generate labels for each frame
    return mfcc.T, [label for _ in range(len(mfcc[0]))]

if __name__ == "__main__":
    mfcc, label = get_mfcc("new_vowels/test/spk1/spk1_aeiou_05.wav", "label")
    print(mfcc.shape, label.shape)