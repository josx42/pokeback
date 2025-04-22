from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    info = {'info': 'App running'}
    print('App running.')
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)