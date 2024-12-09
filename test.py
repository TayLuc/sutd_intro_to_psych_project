import logging
logging.basicConfig(level=logging.DEBUG)

from nrclex import NRCLex
import nltk
nltk.download('punkt_tab')

text = "I am feeling so happy and excited today!"
emotion_analysis = NRCLex(text)
print("Raw Emotion Scores:", emotion_analysis.raw_emotion_scores)
print("Top Emotions:", emotion_analysis.top_emotions)
