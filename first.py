from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def first_json_test():
    return jsonify({'message':'teste funcionou!'})


if __name__ == '__main__':
    app.run(debug=True)




