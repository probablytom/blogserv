import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
import config

config = config.Config()

speech_to_text = SpeechToTextV1(
    username=config.username,
    password=config.password,
    x_watson_learning_opt_out=False
)

print(json.dumps(speech_to_text.models(), indent=2))

with open(join(dirname(__file__), 'speech.wav'), 'rb') as audio_file:
    print(json.dumps(speech_to_text.recognize(
        audio_file, content_type='audio/wav', timestamps=True), indent=2))
