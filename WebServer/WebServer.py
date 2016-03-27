import os
import threading

import tornado.ioloop
import tornado.web
from bson.objectid import ObjectId

from Class import helper
from Class.Log import Log


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RelayHandler(tornado.web.RequestHandler):
    def get(self):
        from Module.Relay import Relay
        object_id = self.get_argument("id", "None")
        relay_action = self.get_argument("type", "None")

        if object_id not in "None":

            if relay_action in "off":
                Relay.set_force_on(object_id, Relay.FORCE_OFF)

            if relay_action in "on":
                Relay.set_force_on(object_id, Relay.FORCE_ON)

            self.redirect('/relay')

        relay_list = Relay.get_relay_object_list()
        self.render("relay.html", relay_list=relay_list)


class WebServer(threading.Thread):
    def __init__(self, port):
        self.port = port
        threading.Thread.__init__(self)
        self.web_path = os.path.dirname(__file__)

    def run(self):
        settings = {
            "static_path": os.path.join(self.web_path, "static"),
            "template_path": os.path.join(self.web_path, "template"),
            "xsrf_cookies": True,
            "debug": True,
            "autoreload": True
        }

        app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/relay", RelayHandler),
        ], **settings)
        app.listen(self.port)

        print("Running")

        tornado.ioloop.IOLoop.current().start()
