from flask import Flask
from flask import render_template, url_for, jsonify
from flask import request, redirect
import pandas as pd
import sys
import sqlalchemy
import pandas as pd
app = Flask('')


def get_db_url():
    print('get_db_url', file=sys.stderr)
    return '{database}://{db_user}:{db_password}@{db_host}:{db_port}/{db_use}{param}'.format(
#            database='mysql+pymysql'
#            db_user='root',
#            db_password='',
#            db_host='127.0.0.1',
#            db_port='3306',
#            db_use='anzan',
#            param='?charset=utf8',
        database='postgresql',
        db_user='cguxtnsgsuoano',
        db_password='db1ddedb395b5394636937c8c056f6986b2e8aef69b4197691f7a489b57b147c',
        db_host='ec2-18-235-107-171.compute-1.amazonaws.com',
        db_port='5432',
        db_use='d7d7jfml0mg7e7',
        param='',
    )


def get_connect_obj():
    print('get_connect_obj', file=sys.stderr)

    db_url = get_db_url()  # 'mysql+pymysql://root:@127.0.0.1:3306/test1230?charset=utf8'
    engine = sqlalchemy.create_engine(db_url)
    return engine


def get_insert_query(table, dct):
    print('get_insert_query', file=sys.stderr)
    columns_str = '('
    values_str = '('
    for k, v in dct.items():
        columns_str += f'{k},'
        if isinstance(v, str):
            s = f"'{v}'"
        else:  # 数値
            s = f'{v}'
        values_str += f'{s},'
    columns_str = columns_str[:-1]  # 最後のカンマ除く
    columns_str += ')'
    values_str = values_str[:-1]  # 最後のカンマ除く
    values_str += ')'

    sql = f'INSERT INTO {table} {columns_str} VALUES {values_str}'
    return sql


@app.route('/')
def index():
    print('index', file=sys.stderr)
    title = 'test'
    return render_template(
        'index.html', 
        title=title,
    )


@app.route('/insert', methods=['POST'])
def insert():  # url for で指定
    print('insert', file=sys.stderr)
    table = 'log'
    print(request.json, file=sys.stderr) 
    sql = get_insert_query(table, request.json)
    print(sql, file=sys.stderr)

    engine = get_connect_obj()
    conn = engine.connect()
    conn.execute(sql)
    del conn, engine

    return redirect('/')


@app.route('/user_data', methods=['GET'])
def user_data():  # url for で指定
    print('/user_data', file=sys.stderr)
    table = 'log'
    sql = f'select date(t) as d, cast(count(*) as float) as play_cnt, cast(sum(judge) as float) as correct_cnt from {table} group by 1;'
    print(sql, file=sys.stderr)
    import pandas as pd
    engine = get_connect_obj()
    conn = engine.connect()    
    df = pd.read_sql_query(
        sql=sql, 
        con=conn)
    del conn, engine

    dct = {
        'xticklabels': list(df['d'].values),
        'play_cnt': list(df['play_cnt'].values),
        'correct_cnt': list(df['correct_cnt'].values),
        }
    print(dct, file=sys.stderr)
    return jsonify(dct)


# 現在不使用 --------------
@app.route('/get_setting', methods=['GET'])
@app.route('/setting', methods=['POST'])
def setting():  # url for で指定
    print('setting', file=sys.stderr)
    table = 'setting'
    print(request.json, file=sys.stderr) 
    dct = request.json
    import datetime
    dct['updated'] = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    sql = get_insert_query(table, dct)
    print(sql, file=sys.stderr)

    engine = get_connect_obj()
    conn = engine.connect()
    conn.execute(sql)
    del conn, engine

    return redirect('/')


def get_setting():  # url for で指定
    print('get_setting', file=sys.stderr)
    user_id = request.args.get('user_id', type=int)
    dct = get_setting_data(user_id)
    print(dct, file=sys.stderr)
    return jsonify(dct)


def get_setting_data(user_id=0):
    print('get_setting_data', user_id, file=sys.stderr)
    table = 'setting'
    sql = f'select * from {table} where user_id = {user_id};'
    print(sql, file=sys.stderr)

    engine = get_connect_obj()
    conn = engine.connect()    
    df = pd.read_sql_query(
        sql=sql, 
        con=conn)
    del conn, engine

    sr = df.iloc[0, :]
    if sr['auto']:
        auto = 'true'
    else:
        auto = 'false'

    dct = {
        'user_id': float(sr['user_id']),
        'len': float(sr['len']),
        'digit1': float(sr['digit1']),
        'digit1_rate': float(sr['digit1_rate']),
        'intervalSec': float(sr['intervalsec']),
        'auto': [auto],
        'improve': sr['improve'],
        }
    return dct


@app.route('/play', methods=['GET'])
def play():
    print('play', file=sys.stderr)
    dct = get_setting_data()
    return render_template(
        'play.html',
        len=int(dct['len']),
        intervalSec=dct['intervalSec'],
        digit1=int(dct['digit1']),
        digit1_rate=dct['digit1_rate'],
        improve=dct['improve'],
        auto=dct['auto']=='true',
    )


if __name__ == "__main__":
    print('main')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
