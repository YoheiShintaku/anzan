from flask import Flask
from flask import render_template, url_for, jsonify
from flask import request, redirect
import pandas as pd
import sys
import sqlalchemy
import pandas as pd

app = Flask('')

@app.route('/')
def index():
    title = 'test'
    return render_template(
        'index.html', 
        title=title,
        )

@app.route('/insert', methods=['POST'])
def insert():  # url for で指定
    print(request.json, file=sys.stderr) 

    columns_str = '('
    values_str = '('
    for k, v in request.json.items():
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

    table = 'log'
    sql = f'INSERT INTO {table} {columns_str} VALUES {values_str}'
    print(sql, file=sys.stderr)
    get_connect_obj().execute(sql)

    return redirect('/')

@app.route('/user_data', methods=['GET'])
def user_data():  # url for で指定
    print('/user_data', file=sys.stderr)
    table = 'log'
    sql = f'select date(t) as d, cast(count(*) as float) as play_cnt, cast(sum(judge) as float) as correct_cnt from {table} group by 1;'
    print(sql, file=sys.stderr)
    import pandas as pd
    df = pd.read_sql_query(
        sql=sql, 
        con=get_connect_obj())
    print(df, file=sys.stderr)

    dct = {
        'xticklabels': list(df['d'].values),
        'play_cnt': list(df['play_cnt'].values),
        'correct_cnt': list(df['correct_cnt'].values),
        }
    print(dct, file=sys.stderr)
    return jsonify(dct)


def get_connect_obj():
    def get_db_url():
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

    db_url = get_db_url()  # 'mysql+pymysql://root:@127.0.0.1:3306/test1230?charset=utf8'
    engine = sqlalchemy.create_engine(db_url)
    conn = engine.connect()
    print('connected')
    return conn
    

if __name__ == "__main__":
    print('main')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
