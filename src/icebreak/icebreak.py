import signal
import subprocess
import asyncio
import sys
import os
import csv

from .propose_topic import propose_topic
from .prompt_speaker import prompt_quiet_speaker
from .least_speaker import least_speaker
from .end_icebreak import end_icebreak

wav_queue = asyncio.Queue()

spk_num = 0

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError('Timeout')

async def process_wav_files():
    while True:
        try:
            # 非同期にキューからファイルを取り出す
            filename = await wav_queue.get()  # asyncio.Queueで非同期にファイルを取り出す
            print(f"Processing {filename}...")

            # wavファイルの処理を行う（例: 音声認識など）
            # ここに処理を書く
            await asyncio.to_thread(process_wav, filename)  # 音声ファイル処理の例

            wav_queue.task_done()  # 処理が完了したことを示す

        except asyncio.QueueEmpty:
            # キューが空の場合は少し待機してから再試行
            await asyncio.sleep(0.1)

def process_wav(filename):
    try:
        # 話者認識
        sidfile="../dialogue-demo/sid/spkid.txt"
        sid_command = ["bash", "../dialogue-demo/sid/test.sh", filename, sidfile]
        subprocess.run(sid_command, check=True)

        with open(sidfile, "r") as f:
            speaker_id = f.read().strip()

        # WAV ファイルの長さを取得
        soxi_command = ["soxi", "-D", filename]
        duration = subprocess.check_output(soxi_command).decode().strip()

        # 文字起こし
        transcribe_command = ["python3", "icebreak/transcribe.py", filename]
        transcribe_result = subprocess.check_output(transcribe_command).decode().strip()

        output_csv="icebreak/data.csv"
        # データを CSV に保存
        csv_exists = os.path.exists(output_csv)
        with open(output_csv, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not csv_exists:
                writer.writerow(["speaker_id", "transcribe_result", "duration"])
            writer.writerow([speaker_id, transcribe_result, duration])
            print(f"Saved to CSV: {speaker_id}, \"{transcribe_result}\", {duration}")


    except Exception as e:
        print(f"Error processing audio: {e}", file=sys.stderr)


async def icebreak_talk(limit_time_sec: int = 300):
    # アイスブレイクのメイン処理
    # 話題を提供 
    # -> メンバーが話す 
    # -> 音声から話者認識し、話した時間を測定 
    # -> ... 
    # -> 会話が止まった（1度目）：一定時間止まったら話している時間が短い人に会話を促す 
    # -> ... 
    # -> 会話が止まった（2度目）：次の話題を提供
    # -> ...
    # 指定された時間になったら終了
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(limit_time_sec)

    flag = 0
    
    try:
        propose_topic()
        while True:

            print("<<Please speak.>>")
            script_path = "icebreak/audio_rec.sh"
            
            process = await asyncio.create_subprocess_exec(
                "bash", script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")

            if process.returncode != 0:
                print(f"Error occurred during recording: {stderr.decode()}")
                if process.returncode == 2:
                    if flag == 0:
                        data_path = "icebreak/data.csv"
                        if os.path.exists(data_path):
                            prompt_quiet_speaker(least_speaker("icebreak/data.csv", spk_num))
                            flag = 1
                    else:
                        propose_topic()
                        flag = 0
                    # print("Recording did not start within the specified timeout.")
                continue

            # ファイル名を取得
            filename = stdout.decode().strip()  # 標準出力からファイル名を取得
            print(f"Recorded file: {filename}")

            # キューに追加
            await wav_queue.put(filename)
            print(f"Added to queue: {filename}")

    except TimeoutError:
        end_icebreak()
        print('Time is up!')
    finally:
        signal.alarm(0)    

def icebreak(num_speakers: int):
    global spk_num  # グローバル変数として話者人数を設定
    spk_num = num_speakers  # 引数として渡された人数を設定

    loop = asyncio.get_event_loop()
    loop.create_task(process_wav_files())  # 非同期でwavファイルの処理を開始
    loop.run_until_complete(icebreak_talk(5 * 60))  # アイスブレイクの処理を同期で実行

