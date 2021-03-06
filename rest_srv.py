from datetime import datetime
import json
import time

from bottle import route, run, template, static_file
import os
from config import config
import sqlite3

ASSETS_JS_PATH = os.path.join('assets/js/')


def dict_factory(cursor, row):
    r = {}
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect(config.db_path, timeout=15)
conn.row_factory = dict_factory

def sql_execute(querry: str, params: dict = None):
    cur = conn.cursor()
    if not params:
        cur.execute(querry)
    else:
        cur.execute(querry, params)
    result = cur.fetchall()
    cur.close()
    return result



@route('/')
def index_page():
    return template('index.html')


@route('/assets/js/<filename>')
def stat_files(filename):
    return static_file(filename, root='assets/js/')


@route('/test')
def test():
    test_result = {'status': 'OK',
                   "val1": 123.22,
                   "val2": 456.01,
                   "current_time": datetime.now().isoformat()
                   }
    # print(json.dumps(test_result, indent=2))
    return json.dumps(test_result)


@route('/')
def index():
    return template('index')


@route('/get_last_sensor_value/<sensor_key>', method='GET')
def get_last_sensor_value(sensor_key):
    querry = """
            select id, 
                device_key, 
                sensor_key, 
                value, 
                timestamp
            from sensor_values
            where device_key = :p_device_key
                and sensor_key = :p_sensor_key
            order by id desc
            limit 1
            """
    params = {'p_device_key': 'esp8266_r01',
              'p_sensor_key': sensor_key}
    res = sql_execute(querry, params)
    res_json = json.dumps(res, indent=2)
    return res_json


@route('/getsensorvalues_json/<sensor_key>', method='GET')
def getrecs(sensor_key):
    mintimestamp = 0
    maxtimestamp = 0
    params = {}
    c = conn.cursor()
    exec_str = """SELECT 
                        round(timestamp/60/10, 0)*60*10 as timestamp, 
                        (max(case  when sensor_key = 'temperature' then value else 0 end) 
                            + max(case  when sensor_key = 'temperature' then value else 0 end))/2 as value_temp,
                        (max(case  when sensor_key = 'humidity' then value else 0 end) 
                            + max(case  when sensor_key = 'humidity' then value else 0 end))/2 as value_hum
                    from sensor_values  
                    where timestamp > :mintimestamp 
                        and sensor_key in ('temperature', 'humidity')
                    group by 
                        round(timestamp/60/10, 0)
                    order by timestamp
                    """
    mintimestamp = time.time() - 3600 * 24
    params = {"mintimestamp": mintimestamp}
    c.execute(exec_str, params)
    results = c.fetchall()
    c.close()
    value_data_temp = []
    value_data_hum = []
    value_labels = []
    json_res = {}
    for v in results:
        # print v
        value_data_temp.append(v['value_temp'])
        value_data_hum.append(v['value_hum'])
        value_labels.append(datetime.fromtimestamp(v['timestamp']).isoformat(' ')[10:])
    # return json.dumps(results)
    json_res['value_data_1'] = value_data_temp
    json_res['value_data_2'] = value_data_hum
    json_res['value_labels'] = value_labels
    return json.dumps(json_res)


if __name__ == '__main__':
    run(host=config.rest_srv_ip_addr, port=config.rest_srv_ip_port)
    conn.close()

