# Copyright (c) 2020 Roman Trapeznikov
import time
from kral2.server.network import LocalServer
from kral2.game.defaultgame import DefaultGame

IPS = 60

if __name__ == '__main__':
    activity = DefaultGame()
    server = LocalServer('0.0.0.0', 43210, activity.spawn_player, activity.try_to_build, activity.try_to_destroy)
    server.objects = activity.objects
    while True:
        now = time.time()
        activity.update()
        server.update()
        time.sleep(max(1/IPS - (time.time() - now), 0))
