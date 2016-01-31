from flask import Flask

import pyex

app = Flask(__name__)


@app.route('/')
def first_json_test():
    return pyex.response
    
if __name__ == '__main__':
    app.run(debug=True)

