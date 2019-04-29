# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
from gevent import monkey
import os
# from server_utils.log import log_setup

patch_status = False
if str(os.environ.get("DEBUG")).lower()!='true' or str(os.environ.get("DEBUG_SERVER")).lower()!='true':
    # 跟gevent的多线程有冲突，容易造成死锁的问题
    monkey.patch_all(thread=False)
    patch_status = True
if os.environ.get("gevent_grpc_support"):
    import grpc.experimental.gevent
    grpc.experimental.gevent.init_gevent()

from gevent.pywsgi import WSGIServer

# from server_utils.geventserver import SingleProcessWSGIServer
from freshProject.freshProject.wsgi import application

PROGRAM = 'daily_fresh'

# log_setup(PROGRAM)


def product():
    ip = '0.0.0.0'
    port = 80
    server = WSGIServer((ip, port), application)
    server.serve_forever()

from django.core.management.commands.runserver import BaseRunserverCommand
def development():
    server = BaseRunserverCommand()
    server.handle(use_ipv6=False, addrport="0.0.0.0:80", use_reloader=True, use_threading=False)


if os.environ.get("DEBUG") and os.environ.get("DEBUG_SERVER"):
    main = development
else:
    main = product

logger.info(">>>>>>>>> RUN MODE >>>>>>>>>>>>：%s" %str(main.__name__))
logger.info(">>>>>>>>> patch_status >>>>>>>>>>>>：%s" %str(patch_status))

if __name__ == '__main__':
    main()