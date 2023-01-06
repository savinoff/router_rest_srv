from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    broker: str = 'mqtt.cloud.yandex.net'
    port: int = 8883
    client_id: str = 'py-registry-srv'
    ca_certs: str = 'certs/rootCA.crt'
    certfile: str = 'certs/reg_cert.pem'
    keyfile: str = 'certs/reg_key.pem'
    topics: List[str] = field(default_factory=list)
    db_path: str = 'db/sensors_values.db'
    rest_srv_ip_addr: str = 'localhost'
    rest_srv_ip_port: int = 3001


config = Config()
config.topics = ['$registries/rrr/#',
                 # device1
                 '$devices/xxx/state/temperature',
                 '$devices/xxx/state/humidity',
                 # esp1
                 '$devices/yyy/state/temperature',
                 '$devices/yyy/state/humidity',
                 # test
                 'test/#']

device_dict = {'xxx': 'esp8266_r01',
               'yyy': 'esp8266_r01'}

if __name__ == '__main__':
    print('Current config:')
    print(config)
