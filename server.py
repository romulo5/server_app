import os
from flask import Flask, request, url_for, flash
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import xls2py


UPLOAD_FOLDER = 'xls2py'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
FUNC_FILE = 'funcoes-raw.xls'
GND_FILE = 'gnd-raw.xls'
UPLOAD_SUCESSFUL = '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>File Uploaded</h1>
            '''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'

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
            flash("File saved.")
            #return UPLOAD_SUCESSFUL
        file = request.files['file-gnd']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], GND_FILE))
            flash("File saved.")
            #return UPLOAD_SUCESSFUL

    return '''
      <!doctype html>
    <title>Upload new File</title>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul class=flashes>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    <h1>Upload de arquivos</h1>

    <form action="" method=post enctype=multipart/form-data>
        <p>Orçamento por Funções</p>
        <input type=file name=file-func>
        <input type=submit value=Enviar>
        <p>Orçamento por GND</p>
        <input type=file name=file-gnd>
        <input type=submit value=Enviar>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

