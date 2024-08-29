from flask import render_template
from code_py.func import get_divase_os
from code_py.config import json_add
import json

def index():
    with open('app.json', 'r') as file:
        json_app_setings = json.load(file)
    if (json_app_setings['start']['number'] == 1):
        return render_template('index.html', json_add=json_add)
    if (json_app_setings['start']['number'] == 0):
        return render_template('install.html', json_add=json_add)
    

def index01():
    with open('app.json', 'r') as file:
        json_app_setings = json.load(file)
    with open('json/version.json', 'r') as file:
        json_version_app = json.load(file)
    return render_template('dist/settings.html', json_add=json_add, json_app_setings=json_app_setings, json_version_app=json_version_app)
    

def index1():
    with open('json/my_sound.json', 'r') as file:
        json_my_sound = json.load(file)
    return render_template('dist/my_sound.html', json_add=json_add, json_my_sound=json_my_sound)
    

def index20910():
    return render_template('install_p/indtall_d.html', json_add=json_add)


def index991():
    with open('app.json', 'r') as file:
        json_app = json.load(file)
    divases = get_divase_os()
    return render_template('install_p/end.html', json_add=json_add, json_app=json_app, divases=divases)