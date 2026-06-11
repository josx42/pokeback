import os, logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort, send_file
from src.resources.updater import update, auto_update
from src.utils.paths import SRC, TYPES, GENERATIONS
from src.utils.manage_json import read_json

load_dotenv()
env = os.getenv('ENV', 'development')
is_dev = env == 'development'
admin_key = os.getenv('ADMIN_KEY')

logging.basicConfig(
    filename = SRC / 'app.log',
    filemode = 'a',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s: %(message)s (At %(name)s)'
    )

auto_update()
update()

app = Flask(__name__)

@app.route('/')
def index():
    info = {'info': 'App running'}
    print('App running.')
    return jsonify(info)


@app.route('/update', methods=['PUT'])
def manual_update():
    received_key = request.headers.get('Authorization')
    if received_key != f'Bearer {admin_key}':
        abort(403)

    update()
    info = {'Info': 'Resources updated'}
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


@app.route('/logs')
def get_log():
    log_file = SRC / 'app.log'
    received_key = request.headers.get('Authorization')
    if received_key != f'Bearer {admin_key}':
        abort(403)
    if not log_file.exists():
        abort(404)

    return send_file(log_file, mimetype="text/plain", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=is_dev, use_reloader=False)