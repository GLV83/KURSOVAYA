from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, send_file
from service.db_handle import *
from service.filesystem import *
from service import data_processor
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['post'])
def login():
    data = request.json
    user = User.select().where(User.login == data['login'])
    if user.count() == 0 or not user.get().check_password(data['password']):
        return jsonify({"msg": "Invalid login or password"})

    user = user.get()
    return jsonify({'login': user.login, 'role': user.role})


@app.route('/add_data', methods=['post'])
def add_data():
    data = request.json
    result = data_processor.add_data(data)
    return jsonify({"result": result})


@app.route('/grapths', methods=['post'])
def get_data():
    result = []
    data = request.json
    df = data_processor.get_data_frame(data)

    for key, value in GRAPTH_TYPES.items():
        if df.empty:
            result.append({'name': value, 'url': ''})
        else:
            __df = df.loc[:, ['start_week', key]]
            fig = plt.figure()
            ax = plt.subplot()
            ax.plot(__df['start_week'], __df[key])
            fig.autofmt_xdate()
            plot_filename = save_plot(fig)
            fig.clear()
            result.append({'name': value, 'url': get_url('grapths', plot_filename)})

    return jsonify(result)


@app.route('/reports', methods=['post'])
def gen_report():
    data = request.json
    df = data_processor.get_data_frame(data)
    filename = save_report(df)
    return jsonify({"url": get_url('reports', filename)})


@app.route('/file/<path:path>')
def send_file(path):
    return send_from_directory('fs', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css/', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js/', path)


if __name__ == '__main__':
    app.run(debug=True)
