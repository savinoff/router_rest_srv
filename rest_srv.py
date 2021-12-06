import json

from bottle import route, run, template


test_result = {'status': 'OK',
               "val1": 123.22,
               "val2": 456.01
               }


@route('/test')
def test():
    print(json.dumps(test_result, indent=2))
    return json.dumps(test_result)


@route('/')
def index():
    return template('index')


if __name__ == '__main__':
    run(host='localhost', port=8080)
