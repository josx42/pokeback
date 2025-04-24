from flask import Flask, jsonify
from src.resources.updater import auto_update

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    info = {'info': 'App running'}
    print('App running.')
    return jsonify(info)

if __name__ == '__main__':
    auto_update()
    app.run(debug=True)