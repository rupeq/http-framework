import os

from example.app import app, api
from example.middleware import MiddlewareExample
from logging_config import configure_logging
from wsgi import WSGIServer

if __name__ == "__main__":
    configure_logging()
    app.register_blueprint(api)
    app.add_middleware(MiddlewareExample())
    server = WSGIServer(app, "127.0.0.1", 8000, hot=True, hot_dir=os.getcwd())
    server.serve_forever()
