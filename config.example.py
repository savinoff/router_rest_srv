from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    broker: str = 'my.keenetic.net'
    port: int = 1883
    client_id: str = f'python-mqtt-999'
    topics: List[str] = field(default_factory=list)
    db_path: str = 'db/sensors_values.db'
    rest_srv_ip_addr: str = 'localhost'
    rest_srv_ip_port: int = 3001

config = Config()
config.topics = ['devices/#',
                 'test/#']

if __name__ == '__main__':
    print('Current config:')
    print(config)
