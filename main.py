from email import message
from operator import le
from flask import Flask, render_template, request, send_file, redirect, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
import os, traceback
from utils.word_editor import *
from utils.db_worker import *
from utils.data_analyse import *
from utils.second_db_parser import *
import lxml.html
from lxml.html import builder

import w


UPLOAD_FOLDER = 'data/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def run():
    return render_template('login.html')

@app.route('/last')
def last():
    return render_template('login.html')

@app.route('/graph.html')
def gr():
    return render_template('graph.html')

@app.route('/', methods=['post', 'get'])
def log_in():
    message = ''
    if request.method == 'POST':
        password = request.form.get('password')
        login = request.form.get('login')
        if find_user(login) == True:
            if check_password(login, password) == True:
                return redirect('/panel')
            else:
                flash("Неверный пароль")
                return render_template('login.html')
        else:
            flash("Такого пользователя нет")
            return render_template('login.html')

@app.route('/panel')
def panel():
    return render_template('main_page.html')

@app.route('/show_table.html')
def my_link():
    w.main(1, ((1, "инфо1"), (2, "инфо2"), (3, "инфо3"), (4, "инфо4"), (5, "инфо5"), (6, "инфо6"), (7, "инфо7"), (8, "инфо8"), (9, "инфо9"), (10, "инфо10"), (11, "инфо11"), (12, "инфо12"), (13, "инфо13")), "Горбунов А. В.")
    path = "picture.docx"
    return send_file(path, as_attachment=True)

@app.route('/panel', methods=['post'])
def get_first_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                flash('Нет выбранного файла')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/info')

@app.route('/info')
def create_table():
    raw_ship_data = load_raw_ship_data()
    raw_fish_data = load_raw_fish_data()
    raw_fish_data = raw_fish_data[raw_fish_data['volume'] != 0]
    merged_data = merge_raw_data(raw_fish_data, raw_ship_data)
    places_count = Analyzer.PlatAnalys.get_id_plat_list(merged_data)
    all_data = pd.DataFrame()
    for i in places_count[:42]:
        sorted_data = Analyzer.CompareAnalys.get_product_and_fish(merged_data, i)
        all_data = all_data.append(sorted_data)
    all_data.to_csv(DATA_PATH + 'Final.csv')
    return render_template('tables_info.html')

@app.route('/table')
def show_table():
    raw_ship_data = load_raw_ship_data()
    raw_fish_data = load_raw_fish_data()
    raw_fish_data = raw_fish_data[raw_fish_data['volume'] != 0]
    merged_data = merge_raw_data(raw_fish_data, raw_ship_data)
    data = []
    places_count = Analyzer.PlatAnalys.get_id_plat_list(merged_data)
    count_place = 1
    for i in places_count[:10]:
        counts = Analyzer.PlatAnalys.get_plat_anomaly_count(merged_data, i)
        data.append([count_place, i, counts])
        count_place += 1
    return render_template('table_show.html', rows=data)

@app.route('/plat_report/<id>')
def show_full_table(id: int):
    raw_ship_data = load_raw_ship_data()
    raw_fish_data = load_raw_fish_data()
    raw_fish_data = raw_fish_data[raw_fish_data['volume'] != 0]
    merged_data = merge_raw_data(raw_fish_data, raw_ship_data)
    finded_data = Analyzer.CompareAnalys.get_product_and_fish(merged_data, int(id))
    data = create_data_list(finded_data)
    report_path = create_report(1, data, 'User')
    return send_from_directory(DATA_PATH, filename='picture.docx', path=report_path)

if __name__ == '__main__':
    app.run(debug=True)