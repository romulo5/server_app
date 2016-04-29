import os

import datetime
import json
from flask import Flask, request, flash, render_template
from flask_bootstrap import Bootstrap


import resources
from sql import mdbtosql, sql


UPLOAD_FOLDER = 'sql'
ALLOWED_EXTENSIONS = {'mdb'}
VERSION_FILE = 'version.json'
DATA_FILE = 'data.mdb'
JSON_RESPONSE_FILE='response.json'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = resources.SECRET_KEY
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def api_response():
    with open(JSON_RESPONSE_FILE, 'r') as f:
        response = json.load(f)
        return json.dumps(response, ensure_ascii=False)



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # Checa se arquivo e valido e atualiza
        data_file = request.files['data-file']
        if data_file and allowed_file(data_file.filename):
            data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], DATA_FILE))
            update_version()
            flash("Base de dados atualizada.", 'success')
            mdbtosql.insert_data()

        else:
            flash("Erro - Base não atualizada.", 'error')

    return render_template('upload.html')


@app.route('/version', methods=['GET'])
def version_response():
    with open(VERSION_FILE, 'r') as f:
        version_data = json.load(f)
        return json.dumps(version_data)


def update_version():
    with open(VERSION_FILE, 'r') as f:
        version_data = json.load(f)
        f.close()
    version_data['date'] = datetime.datetime.now().strftime("%d/%m/%Y")
    version_data['version'] += 1
    with open(VERSION_FILE, 'w+') as f:
        f.write(json.dumps(version_data))
        f.close()

if __name__ == '__main__':
    app.run(debug=True)

