from flask import Flask, render_template, request, jsonify
from utils import cuery
import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


menu = [{"name": 'Главная',"url": "sweet" },
        {"name":'Завод', "url": "manufact"},
        {"name":'Склад', "url": "store"}, 
        {"name":'Найменование сладости', "url": "sweets_types" },
        {"name":'Отоброжение сладости', "url": "sweets_new" }]




@app.route("/")
# @app.route("/index")
def index():
    return "Hello World!"

@app.route("/about")
def about():
    title = 'О сайте'
    return render_template('app/about.html', menu = menu, title = title)

@app.route('/main', methods=['GET', 'POST'])
def main():
    title = 'Главная страница сайта'
    if request.method == 'POST':
        login = request.form.get('login')
        pswd = request.form.get('password')
        email = request.form.get('email')
        p=generate_password_hash(pswd)
        print(check_password_hash(password='123', pwhash = p))
        print(login, pswd, email, p)
    return render_template('app/main.html', title = title, menu = menu)

@app.route('/profile/<username>')
def username():
    return f'Профиль {username}'

@app.route('/sweet', methods =['GET', 'POST'])
def sweet():
    ok = False
    title= 'Добовление сладости'
    if request.method == 'POST':
        name_sweet = request.form['sweet']
        sweet_name = request.form['sweet_name']
        name_cost = request.form['cost']
        name_weight = request.form['weight']
        name_sugar = request.form['sugar']
        name_stores = request.form['store']
        name_manufact = request.form['manufact']
        name_creat_date = request.form['creat_date'].split('-')
        name_end_date = request.form['end_date'].split('-')
        if sweet_name:
            sweet_id = cuery('mybase', '''insert into public.sweets (sweets_types_id, name, cost, weight, manufacturer_id, with_sugar, requires_freezing, production_date, expiration_date) values (%s, %s, %s, %s, %s, %s, %s,%s, %s)
                                returning id''', (int(name_sweet), sweet_name, name_cost, name_weight, int(name_manufact), True if name_sugar == '1' else False, True, datetime.datetime(year = int(name_creat_date[0]), month= int(name_creat_date[1]), day = int(name_creat_date[2]) ), datetime.datetime(year = int(name_end_date[0]), month=int(name_end_date[1]), day= int(name_end_date[2])) ), upd=True, fetch_upd_return=True, debug=True)
            if sweet_id and sweet_id[0]:
                ok = True
        print(name_sweet)
    name_sweet = cuery('mybase', ''' select s."name", s."cost", s.weight, m."name"  from public.sweets s
                        inner join public.manufacturers_storehouses ms on s.id= ms.manufacturers_id
                        inner join public.manufacturers m on ms.manufacturers_id = m.id ''')

    sweet_type=cuery('mybase', '''select st.id, st."name"  from public.sweets_types st ''')
    name_manuf = cuery('mybase', '''select m.id as "m_id", m."name" as "m_name" from public.manufacturers m  ''')
    name_store = cuery('mybase', ''' select s.id as "s_id", s."name"  as "s_name" from public.storehouses s ''')
    return render_template('app/sweet.html', title = title, ok = ok, menu= menu, name_sweet= name_sweet, name_manuf= name_manuf, name_store=name_store, sweet_type=sweet_type)

@app.route('/store', methods =['GET'])
def store():
    title= 'Таблица складов:'
    if request.method =='GET':
        st_get= cuery('mybase', ''' select s."name",s.city, s.id from public.storehouses s ''')
    return render_template('app/store.html', title=title, st_get=st_get, menu=menu)
    
@app.route('/manufact', methods =['GET'])
def manufact():
    title= 'Таблица складов:'
    if request.method =='GET':
        mn = cuery('mybase', '''select m."name", m.city, m.id  from public.manufacturers m ''')
    return render_template('app/manufact.html', title=title, mn=mn, menu=menu)

@app.route('/manufact_info', methods = ['POST', 'GET'])
def manufact_info():
    if request.method == 'POST':
        ma_in = request.form['id']
        ma_info = cuery('mybase', '''select m."name", m.phone, m.adress, m.city , m.country from public.manufacturers m where m.id = %s''', (ma_in))
        return jsonify(ma_info=ma_info)
    
@app.route('/store_info', methods = ['POST', 'GET'])
def store_info():
    st_in= request.form['id']
    st_info = cuery('mybase', '''select s."name", s.adress, s.city, s.country  from  public.storehouses s where s.id = %s''', (st_in))
    return jsonify(st_info=st_info)

@app.route('/sweets_types',methods = ['POST', 'GET'])
def sweets_types():
    title = 'Таблица типов сладости:'
    if request.method == 'GET':
        sw_t = cuery('mybase', '''select st."name"  from public.sweets_types st ''')
        return render_template('app/sweets_types.html', title=title, sw_t=sw_t, menu=menu)
    
@app.route('/sweets_new',methods = ['POST', 'GET'])
def sweets_new():
    title = 'Сладости и их характеристики:'
    if request.method == 'GET':
        sw_n = cuery('mybase', '''select s."name", s."cost", s.weight, s.id from  public.sweets s ''')
        return render_template('app/sweets_new.html', title=title, sw_n=sw_n, menu=menu)

@app.route('/sweets_info', methods = ['POST', 'GET'])
def sweets_info():
    sw_in= request.form['id']
    sw_info = cuery('mybase', '''select s."name", s."cost", s.weight, s.with_sugar, s.requires_freezing, s.production_date, s.expiration_date  from public.sweets s where s.id = %s''', (sw_in,))
    return jsonify(sw_info=sw_info)


if __name__=='__main__':
    app.run(debug = True, port = 5001)
