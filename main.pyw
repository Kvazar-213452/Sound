from flask import Flask, send_from_directory, request, jsonify
import threading
import json
import os
import signal
import socket
from code_py.func import receive_sound_paley
from code_py.page import index, index01, index1, index20910, index991
from code_py.func_app import check_heartbeat, start_executable, terminate_process, heartbeat
from code_py.post import receive_sound_paley1, receive_sound_paley8, stop_def, convert_mp3, convert_mp4, code1, code2

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

with open('app.json', 'r') as file:
    chek = json.load(file)

if chek['version_sound']['vers'] != 20:
    os.kill(os.getpid(), signal.SIGINT)

if chek['core']['version'] != 5:
    os.kill(os.getpid(), signal.SIGINT)

if chek.get('Created') != "Article Kvazar":
    os.kill(os.getpid(), signal.SIGINT)


app = Flask(__name__)

@app.route('/')
def route_1():
    return index()

@app.route('/settings')
def route_2():
    return index01()

@app.route('/mu_m')
def route_3():
    return index1()
    
@app.route('/instal_dependens')
def route_7():
    return index20910()

@app.route('/instal_end')
def route_8():
    return index991()

@app.route('/add_sound', methods=['POST'])
def post_1():
    return receive_sound_paley1()

@app.route('/del_music', methods=['POST'])
def post_2():
    return receive_sound_paley8()

@app.route('/stop_def', methods=['POST'])
def post_4():
    return stop_def()

@app.route('/convert_mp3', methods=['POST'])
def post_5():
    return convert_mp3()

@app.route('/convert_mp4', methods=['POST'])
def post_6():
    return convert_mp4()

@app.route('/end_install', methods=['POST'])
def post_7():
    return code1()

@app.route('/app_json_1', methods=['POST'])
def post_8():
    return code2()

@app.route('/sound_paley', methods=['POST'])
def post_9():
    return receive_sound_paley()

@app.route('/heartbeat', methods=['POST'])
def post_10():
    return heartbeat()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    text_input = data.get('textInput')

    with open('app.json', 'r') as file:
        data_1 = json.load(file) 

    data_1['divase']['micro'] = int(text_input)

    with open('app.json', 'w') as file:
        json.dump(data_1, file, indent=4)

    return jsonify({'message': 'Data received successfully', 'receivedData': text_input})

@app.route('/sound/<path:filename>')
def serve_sound(filename):
    return send_from_directory('../sound', filename)

if __name__ == '__main__':
    port = find_free_port()

    html_content = f'<style>iframe{{position: fixed;height: 100%;width: 100%;top: 0%;left: 0%;}}</style><iframe src="http://127.0.0.1:{port}/" frameborder="0"></iframe>'

    file_content = f'''name = Sound_panel
window_h = 800
window_w = 1000
html = "{html_content}"
    '''

    file_path = 'start.article'

    with open(file_path, 'w') as file:
        file.write(file_content)


    start_executable()
    threading.Thread(target=check_heartbeat, daemon=True).start()
    
    try:
        app.run(debug=True, port=port)
    finally:
        terminate_process()


