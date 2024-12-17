import os
import glob

def clear():
    # inputディレクトリのパス
    input_dir = os.path.join(os.path.dirname(__file__), 'input')
    
    # inputディレクトリ内のすべての.wavファイルを取得
    wav_files = glob.glob(os.path.join(input_dir, '*.wav'))
    
    # 各.wavファイルを削除
    for wav_file in wav_files:
        try:
            os.remove(wav_file)  # ファイルを削除
            print(f"Deleted: {wav_file}")
        except Exception as e:
            print(f"Error deleting {wav_file}: {e}")
    
    # icebreakディレクトリ内のdata.csvファイルのパス
    data_csv = os.path.join(os.path.dirname(__file__), 'icebreak', 'data.csv')
    
    # data.csvが存在する場合、削除
    if os.path.exists(data_csv):
        try:
            os.remove(data_csv)  # ファイルを削除
            print(f"Deleted: {data_csv}")
        except Exception as e:
            print(f"Error deleting {data_csv}: {e}")