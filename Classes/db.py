from config import config
import sqlite3
import time

class DBase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connected = 0

    def connect(self):
        print(f'Connecting to {self.db_file} ...')
        self.conn = sqlite3.connect(self.db_file, timeout=15)
        self.connected = 1
        print('Connected OK')

    def add_sensor_value(self, device_key: str, sensor_key: str, value: float, timestamp: int = None):
        if self.connected != 1:
            self.connect()
        if not timestamp:
            timestamp = time.time()
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO sensor_values (device_key, sensor_key, value, timestamp)"
                      "VALUES (?,?,?,?)", (device_key, sensor_key, value, timestamp))
        except sqlite3.OperationalError:
            self.create_db()
            c.execute("INSERT INTO sensor_values (device_key, sensor_key, value, timestamp)"
                      "VALUES (?,?,?,?)", (device_key, sensor_key, value, timestamp))
        new_id = c.lastrowid
        self.conn.commit()
        c.close()
        print(f'added record id: {new_id}')
        return 0

    def get_sensors_values(self):
        c = self.conn.cursor()
        res = list(c.execute('SELECT * FROM sensor_values'))
        c.close()
        return res

    def create_db(self):
        if self.connected != 1:
            self.connect()
        res = self.conn.execute("""Create table sensor_values (
                                id          integer primary key,
                                device_key  char(20) not null,
                                sensor_key  char(20) not null,
                                value       REAL not null,
                                timestamp   REAL not null)
                                """)
        print(f'Created table table sensor_values', res)
        self.conn.commit()
        return 0

db = DBase(config.db_path)
db.connect()


if __name__ == '__main__':
    print(config)
    db = DBase(config.db_path)
    # db.create_db()
    db.add_sensor_value('test_device', 'test_sensor', 15.0)
    db.get_sensors_values()

