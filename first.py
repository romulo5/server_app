from flask import Flask
import xls2py

app = Flask(__name__)


@app.route('/')
def api_response():
    return xls2py.convert()
    
@app.route('/update')
def update_xls():
    return

if __name__ == '__main__':
    app.run(debug=True)

