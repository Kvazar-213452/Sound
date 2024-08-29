from code_py.func import stop_all_streams, generate_random_filename, play_audio_0, get_device_index_by_name
import json
from pydub import AudioSegment
from flask import request
import os
import subprocess

def receive_sound_paley1():
    text_input = request.form['textInput']
    file_input = request.files['fileInput']

    json_path = 'json/my_sound.json'
    json_data = []

    random_filename = generate_random_filename() + os.path.splitext(file_input.filename)[1]
    file_path = os.path.join('sound', random_filename)
    
    file_input.save(file_path)
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)

    new_entry = {
        "name": text_input,
        "file": "sound/" + random_filename
    }
    json_data.append(new_entry)

    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    return 'good'


def receive_sound_paley8():
    data = request.json
    audio_path = data.get('name')
    
    json_path = 'json/my_sound.json'
    file_to_delete = os.path.join(audio_path)
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)

        for entry in json_data:
            if entry.get('file') == audio_path:
                json_data.remove(entry)
                break

        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    return 'good'


def stop_def():
    stop_all_streams()
    return 'Received', 200


def convert_mp3():
    file_input = request.files['fileInput']
    
    mp3_file_path = "temp/mp3/input.mp3"
    file_input.save(mp3_file_path)
    
    wav_file_path = "temp/mp3/output.wav"
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")

    with open(wav_file_path, 'rb') as f:
        converted_wav = f.read()
    
    return converted_wav, 200, {'Content-Type': 'audio/wav'}


def convert_mp4():
    file_input = request.files['fileInput']
    
    mp4_file_path = "temp/mp4/input.mp4"
    file_input.save(mp4_file_path)
    
    wav_file_path = "temp/mp4/output.wav"
    audio = AudioSegment.from_file(mp4_file_path, format="mp4")
    audio.export(wav_file_path, format="wav")

    with open(wav_file_path, 'rb') as f:
        converted_wav = f.read()
    
    return converted_wav, 200, {'Content-Type': 'audio/wav'}



def code1():
    data = request.json
    app = data.get('data')
    if (app == 1):
        with open('app.json', 'r') as file:
            json_app = json.load(file)
        current_directory = os.getcwd()
        exe_path = os.path.join(current_directory, "install", json_app['start']['install_exe'])
        subprocess.run(exe_path, shell=True)
        return 'ok'
    


def code2():
    data = request.json
    app = data.get('data')
    if (app == 1):
        with open('app.json', 'r') as file:
            data = json.load(file)

        data['start']['number'] = 1

        with open('app.json', 'w') as file:
            json.dump(data, file, indent=4)

        device_name = "Virtual"
        device_index = get_device_index_by_name(device_name, skip=1)
        if device_index is not None:
            index_micro = device_index

        with open('app.json', 'r') as file:
            data = json.load(file)

        data['divase']['micro'] = index_micro

        with open('app.json', 'w') as file:
            json.dump(data, file, indent=4)

        return 'ok'
    

