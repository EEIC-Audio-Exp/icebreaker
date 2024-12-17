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
    record_wav_path = sorted(os.listdir('./input'))[-1]
    if os.path.exists(record_wav_path):
        tension = get_tension('./input.wav')
        comical = 100 - tension
        nearest_index = (df['tension'] - comical).abs().idxmin()
        topic = df.loc[nearest_index, 'topic']
    else:
        topic_list = topic_df['topic'].to_list()
        topic = random.choice(topic_list)    
    return topic

def propose_topic():
    topic = determine_topic()
    dynamic_value_manager.set_value(topic)
    speak_str = f"では、次は{topic} について話しましょう！"
    os.system(mk_jtalk_command(speak_str))

