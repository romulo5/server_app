import os

import datetime

import json

from flask import Flask, request, flash, render_template

from flask_bootstrap import Bootstrap

import resources

from sql import updatesql, sql


UPLOAD_FOLDER = resources.UPLOAD_FOLDER
VERSION_FILE = resources.VERSION_FILE
JSON_RESPONSE_FILE=resources.JSON_RESPONSE_FILE
DATA_FILE = 'datadb.sql'
ALLOWED_EXTENSIONS = {'sql'}

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
            updatesql.import_data()
            sql.save_json_data_file()
            flash("Base de dados atualizada.", 'success')

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

#if __name__ == '__main__':
 #   app.run()

