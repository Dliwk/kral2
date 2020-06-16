# Copyright (c) 2020 Roman Trapeznikov
import time
from kral2.server.network import LocalServer
from kral2.game.defaultgame import DefaultGame
import json

IPS = 60

if __name__ == '__main__':
    activity = DefaultGame()
    server = LocalServer('0.0.0.0', 43210, activity.spawn_player, activity.try_to_build, activity.try_to_destroy)
    server.objects = activity.objects
    # Use it for map loading
    # f = open('map-1592340467.0276136.kral2.mapdump')
    # mapdump = json.loads(f.read())
    # f.close()
    # activity.load_objects(mapdump)
    try:
        while True:
            now = time.time()
            activity.update()
            server.update()
            time.sleep(max(1/IPS - (time.time() - now), 0))
    except BaseException as e:
        fname = f'map-{time.time()}.kral2.mapdump'
        f = open(fname, 'w')
        f.write(server.mapdump())
        f.close()
        print(f'finishing... map at {fname}')
        raise e
