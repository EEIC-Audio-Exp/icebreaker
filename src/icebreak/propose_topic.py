import os
import sys
import random
import pandas as pd

sys.path.append('..')
from dynamic_manager import dynamic_value_manager
from .speak import mk_jtalk_command


script_dir = os.path.dirname(os.path.abspath(__file__))
topics = pd.read_csv(os.path.join(script_dir, 'topics.csv'))['topic'].tolist()

def propose_topic():
    topic = random.choice(topics)
    dynamic_value_manager.set_value(topic)
    speak_str = f"では、次は{topic} について話しましょう！"
    os.system(mk_jtalk_command(speak_str))

