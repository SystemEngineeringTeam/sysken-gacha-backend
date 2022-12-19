#!/usr/bin/env python3
import os

import connexion
from dotenv import load_dotenv
from flask import logging

from openapi_server import encoder
from openapi_server.db import setup_db

load_dotenv()
try:
    test = os.environ["JWT_SECRET"]
except KeyError:
    print("JWT_SECRET を設定してください")
    exit(1)

setup_db()

# JWT_SECRETはトークン発行に必要な鍵。
# 必ず設定されている必要がある
# added from https://github.com/spec-first/connexion/blob/main/examples/openapi3/reverseproxy/app.py
class ReverseProxied:
    """Wrap the application in this middleware and configure the
    reverse proxy to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.
    In nginx:
    location /proxied {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-Path /proxied;
    }
    :param app: the WSGI application
    :param script_name: override the default script name (path)
    :param scheme: override the default scheme
    :param server: override the default server
    """

    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        logging.warning(
            "this demo is not secure by default!! "
            "You'll want to make sure these headers are coming from your proxy, "
            "and not directly from users on the web!"
        )
        script_name = environ.get("HTTP_X_FORWARDED_PATH", "") or self.script_name
        if script_name:
            environ["SCRIPT_NAME"] = "/" + script_name.lstrip("/")
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO_OLD"] = path_info
                environ["PATH_INFO"] = path_info[len(script_name):]
        scheme = environ.get("HTTP_X_SCHEME", "") or self.scheme
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        server = environ.get("HTTP_X_FORWARDED_SERVER", "") or self.server
        if server:
            environ["HTTP_HOST"] = server
        return self.app(environ, start_response)


def main():
    app = connexion.App(__name__, specification_dir="./openapi/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        "openapi.yaml", arguments={"title": "SyskenGacha-backend"}, pythonic_params=True
    )
    flask_app = app.app
    proxied = ReverseProxied(flask_app)
    app.wsgi_app = proxied

    app.run(port=8080)

# TODO: DBテーブル作成のインライン化
# 環境変数未設定時にプロンプトを表示

if __name__ == "__main__":
    main()
