# Copyright (c) 2020 Roman Trapeznikov

from kral2.client.network import LocalClient
from kral2.client.graphics.thread import GraphicsThread

if __name__ == '__main__':
    client = LocalClient('127.0.0.1', 43210, name='Player')
    gt = GraphicsThread(client)
    gt.start()
