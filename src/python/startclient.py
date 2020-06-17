# Copyright (c) 2020 Roman Trapeznikov

import os
import yaml
from kral2.client.network import LocalClient
from kral2.client.graphics.thread import GraphicsThread

if __name__ == '__main__':
    config = {'ip': '127.0.0.1', 'port': 43210, 'name': 'Player'}
    if os.path.exists('../client_config.yaml'):
        with open('../client_config.yaml') as conf:
            data = conf.read()
        config = yaml.load(data, yaml.Loader)
    client = LocalClient(config['ip'], config['port'], name=config['name'])
    gt = GraphicsThread(client)
    gt.start()
