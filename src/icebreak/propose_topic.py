import os
import random
import pandas as pd

from speak import mk_jtalk_command

script_dir = os.path.dirname(os.path.abspath(__file__))
topics = pd.read_csv(os.path.join(script_dir, 'topics.csv'))['topic'].tolist()

def propose_topic():
    topic = random.choice(topics)
    speak_str = f"では、次は{topic} について話しましょう！"
    os.system(mk_jtalk_command(speak_str))


if __name__ == '__main__':
    for i in range(5):
        propose_topic()
