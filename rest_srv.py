from datetime import datetime
import json
import time

from bottle import route, run, template, static_file
import os
from config import config
import sqlite3
from Classes.db import db

ASSETS_JS_PATH = os.path.join('assets/js/')
"""
тестовые запросы:
wget http://localhost:3001/add_sensor_value/test_device/humidity/90
wget http://localhost:3001/add_sensor_value/test_device/temperature/20.5
wget http://localhost:3001/add_sensor_value/test_device/temperature/tttt
wget http://localhost:3001/add_sensor_value/test_device/temperature/20,5


curl http://localhost:3001/v2/add_sensor_value/TTTTBot/puffs/22.11
curl http://localhost:3001/v2/add_sensor_value/TTTTBot/puffs/22.17/1685208785
curl http://localhost:3001/v2/get_sensor_values/TTTTBot/puffs
curl http://localhost:3001/v2/get_sensor_values/TTTTBot/puffs/10
curl http://localhost:3001/v2/sensors
curl http://localhost:3001/v2/devices

"""

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

@route('/add_sensor_value/<device_key>/<sensor_key>/<value>', method='GET')
def add_sensor_value(device_key: str, sensor_key: str, value: float ):
    try:
        db.add_sensor_value(str(device_key), str(sensor_key), float(str(value).replace(',', '.')))
    except Exception as e:
        print(f'Error in writing sensor values to db {e}\nParameters: {device_key=} {sensor_key=} {value=}')
    return 'OK'

@route('/v2/add_sensor_value/<device_key>/<sensor_key>/<value>', method='GET')
@route('/v2/add_sensor_value/<device_key>/<sensor_key>/<value>/<timestamp>', method='GET')
def add_sensor_value(device_key: str, sensor_key: str, value: float, timestamp: float = None):
    """ insert sensor values
    """
    try:
        db.add_sensor_value(str(device_key),
                            str(sensor_key),
                            float(str(value).replace(',', '.')),
                            float(str(timestamp).replace(',', '.')) if timestamp else None)
    except Exception as e:
        print(f'Error in writing sensor values to db {e}\nParameters: {device_key=} {sensor_key=} {value=}')
        return 'Error XDVS-RS-002'
    return 'OK'

@route('/v2/get_sensor_values/<device_key>/<sensor_key>', method='GET')
@route('/v2/get_sensor_values/<device_key>/<sensor_key>/<limit>', method='GET')
def get_last_sensor_value(device_key, sensor_key, limit=1):
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
            limit :p_limit
            """
    params = {'p_device_key': device_key,
              'p_sensor_key': sensor_key,
              'p_limit': limit}
    res = sql_execute(querry, params)
    res_json = json.dumps(res, indent=2)
    return res_json

@route('/v2/devices')
def devices():
    querry = """
            select device_key,
                count(*) as cnt,
                max(timestamp) as max_timestamp,
                min(timestamp) as min_timestamp
            from sensor_values
            group by device_key
            order by 1
            """
    params = {}
    res = sql_execute(querry, params)
    res_json = json.dumps(res, indent=2)
    return res_json

@route('/v2/sensors')
def sensors():
    querry = """
            select device_key,
                sensor_key,
                count(*) as cnt,
                max(timestamp) as max_timestamp,
                min(timestamp) as min_timestamp
            from sensor_values
            group by device_key, sensor_key
            order by 1
            """
    params = {}
    res = sql_execute(querry, params)
    res_json = json.dumps(res, indent=2)
    return res_json

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
