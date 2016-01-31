from flask import Flask
import ex2py

app = Flask(__name__)


@app.route('/')
def api_response():
    return ex2py.convert_xls2py()
    
@app.route('/update')
def update_xls():
    return

if __name__ == '__main__':
    app.run(debug=True)

