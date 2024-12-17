import os
import sys
import random
import pandas as pd

sys.path.append('..')
from dynamic_manager import dynamic_value_manager
from .speak import mk_jtalk_command
from .get_emotion.get_tension  import get_tension


script_dir = os.path.dirname(os.path.abspath(__file__))
topic_df = pd.read_csv(os.path.join(script_dir, 'topics.csv'))

def determine_topic() -> str:
    global topic_df
    record_wav_paths = sorted(os.listdir('./input'))
    if record_wav_paths:
        tension = get_tension(f'./input/{record_wav_paths[-1]}')
        print(f"Tension is {tension}!!")
        comical = 100 - tension + random.randint(-20, 20)
        nearest_index = (topic_df['tension'] - comical).abs().idxmin()
        topic = topic_df.loc[nearest_index, 'topic']
        topic_df = topic_df.drop(index=nearest_index)
    else:
        random_row = topic_df.sample(n=1)
        index = random_row.index[0]
        topic_df = topic_df.drop(index=index)
        print(random_row)
        topic = random_row['topic'].values[0]
        
    return topic

def propose_topic():
    topic = determine_topic()
    dynamic_value_manager.set_value(topic)
    speak_str = f"では、次は{topic} について話しましょう！"
    os.system(mk_jtalk_command(speak_str))
