import signal

from propose_topic import propose_topic
from prompt_speaker import prompt_quiet_speaker

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError('Timeout')

def icebreak(limit_time_sec: int = 300):
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
    
    try:
        while True:
            propose_topic()
            
            prompt_quiet_speaker()

    except TimeoutError:
        print('Time is up!')
    finally:
        signal.alarm(0)    
    
if __name__ == "__main__":
    icebreak(20)