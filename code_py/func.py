import json
from flask import request, jsonify
import random
import string
import pyaudio
import wave
import threading
import sounddevice as sd

def get_divase_os():
    devices = sd.query_devices()
    list_divase = []
    for idx, device in enumerate(devices):
        device_info = {
            "divase": f"The device {idx}: {device['name']}, {device['hostapi']}"
        }
        list_divase.append(device_info)
    return list_divase


def audio():
    with open('app.json', 'r') as file:
        json_app_setings = json.load(file)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    # Вибираємо пристрої за їх індексами
    input_device_index = json_app_setings['divase']['headph']  # Індекс вхідного пристрою (мікрофон)
    output_device_index = json_app_setings['divase']['micro']  # Індекс вихідного пристрою (динамік)

    stream_in = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=input_device_index)

    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK,
                        output_device_index=output_device_index)

    try:
        while True:
            data = stream_in.read(CHUNK)
            stream_out.write(data)

    except KeyboardInterrupt:
        print("Recording stopped by user")

    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()

    p.terminate()

audio_thread = threading.Thread(target=audio)
audio_thread.start()

def stop_all_streams():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        p.terminate()


def generate_random_filename():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return random_string

def play_audio_0(filename, device_index):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()


def get_device_index_by_name(name, skip=1):
    p = pyaudio.PyAudio()
    count = 0
    index = None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if name.lower() in info["name"].lower():  
            count += 1
            if count > skip:
                index = i
                break
    p.terminate()
    return index


def play_audio(filename, device_indexes):
    global stop_audio_flag

    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    streams = []
    for device_index in device_indexes:
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=device_index)
        streams.append(stream)

    data = wf.readframes(chunk)

    while data and not stop_audio_flag:
        for stream in streams:
            stream.write(data)
        data = wf.readframes(chunk)

    for stream in streams:
        stream.stop_stream()
        stream.close()

    p.terminate()

def receive_sound_paley():
    global audio_thread, stop_audio_flag

    data = request.get_json()
    name = data.get("name")
    action = data.get("action")
    current_time = data.get("currentTime")

    if action == "play":
        stop_audio_flag = False
        audio_thread = threading.Thread(target=play_audio, args=(name, [6]))
        audio_thread.start()
    elif action == "pause" or action == "stop":
        stop_audio_flag = True
        if audio_thread:
            audio_thread.join()

    return jsonify({"status": "success"})


