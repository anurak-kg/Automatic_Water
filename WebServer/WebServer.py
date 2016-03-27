import threading

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class RelayHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Relay!")


class WebServer(threading.Thread):
    def __init__(self, port):
        self.port = port
        threading.Thread.__init__(self)

    def run(self):
        app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/relay", RelayHandler),
        ])
        app.listen(self.port)
        print("Running")
        tornado.ioloop.IOLoop.current().start()
