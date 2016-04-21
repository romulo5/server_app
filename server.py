import os

import datetime

import json

from flask import Flask, request, flash, render_template

from flask_bootstrap import Bootstrap

import xls2py


UPLOAD_FOLDER = '/home/romulofloresta/server_app/xls2py'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
FUNC_FILE = 'funcoes-raw.xls'
GND_FILE = 'gnd-raw.xls'
JSON_FILE = 'server_app/version.json'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def api_response():
    return xls2py.convert()


@app.route('/upload', methods=['GET', 'POST'])
def upload_xls():
    if request.method == 'POST':
        file = request.files['file-func']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], FUNC_FILE))
            flash("Arquivo de Funções Atualizado.")

        file = request.files['file-gnd']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], GND_FILE))
            flash("Arquivo GND Atualizado.")
        update_version()
    return render_template('upload.html')


@app.route('/version', methods=['GET'])
def version_response():
    with open(JSON_FILE, 'r') as f:
        version_data = json.load(f)
        return json.dumps(version_data)


def update_version():
    with open(JSON_FILE, 'r') as f:
        version_data = json.load(f)
        f.close()
    version_data['update_time'] = datetime.datetime.now().strftime("%x - %H:%M:%S")
    version_data['version'] += 1
    with open(JSON_FILE, 'w+') as f:
        f.write(json.dumps(version_data))
        f.close()

#if __name__ == '__main__':
 #   app.run()

