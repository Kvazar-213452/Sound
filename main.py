from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import tempfile

DEVICE_INDEX = 46

text = input("text ")

mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
tts = gTTS(text=text, lang="uk")
tts.save(mp3_file)

audio = AudioSegment.from_mp3(mp3_file)
audio = audio.set_channels(1).set_frame_rate(44100)

samples = np.array(audio.get_array_of_samples())

sd.play(
    samples,
    samplerate=audio.frame_rate,
    device=DEVICE_INDEX
)
sd.wait()
