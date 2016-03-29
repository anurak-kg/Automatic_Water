import os
import threading

import tornado.ioloop
import tornado.web
import demjson
from bson.objectid import ObjectId

from Class import helper
from Class.Log import Log
from Class.RedisDatabase import RedisDatabase


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RealTimeChartHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("realtime_chart.html")


class AjaxDataHandler(tornado.web.RequestHandler):
    def get(self):
        redis = RedisDatabase()
        type_data = self.get_argument("type", "None")
        if type_data in "real":
            self.write(demjson.encode({"water_level": redis.get_water_level()}))
        # self.render("realtime_chart.html")


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
            (r"/real", RealTimeChartHandler),
            (r"/ajax_data", AjaxDataHandler),
        ], **settings)
        app.listen(self.port)

        print("Running")

        tornado.ioloop.IOLoop.current().start()
