from flask import Flask, jsonify, request
from src.resources.updater import update, auto_update
from src.utils.paths import TYPES, GENERATIONS
from src.utils.manage_json import read_json

app = Flask(__name__)

@app.route('/')
def index():
    info = {'info': 'App running'}
    print('App running.')
    return jsonify(info)


@app.route('/update')
def manual_update():
    update(from_scratch = True)
    info = {'info': 'Resources updated'}
    return jsonify(info)


@app.route('/types/<name>')
@app.route('/types/<name>/accumulated')
def get_type(name):
    suffix = '_accumulated' if request.path.endswith('accumulated') else ''
    resource = read_json(TYPES / f'{name}{suffix}.json')
    return jsonify(resource)


@app.route('/generations/<int:number>/partial')
@app.route('/generations/<int:number>/partial/accumulated')
def get_generation_monotypes(number):
    suffix = '_accumulated' if request.path.endswith('accumulated') else ''
    resource = read_json(GENERATIONS / f'gen_{number}_partial{suffix}.json')
    return jsonify(resource)

@app.route('/generations/<int:number>/strict')
@app.route('/generations/<int:number>/strict/accumulated')
def get_generation_duals(number):
    suffix = '_accumulated' if request.path.endswith('accumulated') else ''
    resource = read_json(GENERATIONS / f'gen_{number}_strict{suffix}.json')
    return jsonify(resource)


if __name__ == '__main__':
    auto_update()
    app.run(debug=True)