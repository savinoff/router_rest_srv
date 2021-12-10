from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    broker: str = 'my.keenetic.net'
    port: int = 1883
    client_id: str = f'python-mqtt-999'
    topics: List[str] = field(default_factory=list)


config = Config()
config.topics = ['devices/#',
                 'test/#']

if __name__ == '__main__':
    print('Current config:')
    print(config)
