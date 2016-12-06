import os
import traceback
import urllib2
import urllib
import re

from contextlib import closing

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

import hashlib

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

MATHOID_URL = os.environ['MATHOID_URL']
MATHOID_CACHE_ROOT = os.environ['MATHOID_CACHE']
MATHOID_SERVE_URL = os.environ['MATHOID_SERVE_URL']


class MathoidException(Exception):
    pass


class MainHandler(tornado.web.RequestHandler):
    def is_cached(self, formula_filename):
        path = os.path.join(MATHOID_CACHE_ROOT, formula_filename)
        return os.path.exists(path)

    def write_cache(self, formula_filename, raw_png_data):
        filename = os.path.join(MATHOID_CACHE_ROOT, formula_filename)
        with open(filename, 'wb') as image:
            image.write(raw_png_data)

    def generate_filename(self):
        try:
            formula = tornado.escape.xhtml_unescape(self.get_argument('text')).encode('utf-8')
            print formula
            formula = formula.replace('!math ', '', 1)
            filename = hashlib.md5(formula).hexdigest() + ".png"

            if self.is_cached(filename):
                return filename

            try:
                request = urllib2.urlopen(MATHOID_URL, urllib.urlencode({
                    'q': formula,
                    'type': 'tex'
                }))
            except urllib2.HTTPError as e:
                if e.code == 400:
                    data = json.loads(e.read())
                    message = '\n'.join(data['detail'])
                    raise MathoidException(message)
                else:
                    return MathoidException('Failed to connect to Mathoid for: %s' % formula)
            except Exception:
                traceback.print_exc()
                return MathoidException('Failed to connect to Mathoid for: %s' % formula)
        except Exception as error:
            traceback.print_exc()
            raise MathoidException('Unspecified Mathoid error')

        with closing(request) as f:
            data = f.read()
            try:
                data = json.loads(data)
            except ValueError:
                raise MathoidException('Invalid Mathoid response for: %s\n%s' % (formula, data))

        if not data['success']:
            raise MathoidException('Mathoid failure for: %s\n%s', formula, data)

        if 'png' not in data:
            raise MathoidException('Mathoid did not provide image data')

        raw_png_data = bytearray(data['png']['data'])
        self.write_cache(filename, raw_png_data)
        return filename

    def post(self):
        try:
            text = MATHOID_SERVE_URL + self.generate_filename()
        except Exception as error:
            text = error.message
        self.write(json.dumps({'text': text}))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/typeset", MainHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": MATHOID_CACHE_ROOT}),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
