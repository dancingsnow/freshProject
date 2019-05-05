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
from freshProject.wsgi import application

PROGRAM = 'daily_fresh'

# log_setup(PROGRAM)
"""
一、 django-runserver的部分实现(基类)
        - 实现了AutoReload机制（可设置）
        - 不包含静态文件的处理handler
        - 可处理普通接口，不支持静态文件/static/路径访问

    from django.core.management.commands.runserver import BaseRunserverCommand

    server = BaseRunserverCommand()
    server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)


二、django-runserver的完全实现
        - 实现了AutoReload机制（可设置）
        - 并且添加了StaticFilesHandler的静态文件的处理handler，
        - 当服务器启动，等于 Python manage.py runserver

    from django.contrib.staticfiles.management.commands.runserver import Command as DebugServer
    server = DebugServer()
    server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)

三、gevent的WSGIServer的实现
        - 协程异步接口实现
        - 静态文件处理未实现？ todo 待确认
        
    from gevent.pywsgi import WSGIServer
    from freshProject.wsgi import application

    server = WSGIServer(("0.0.0.0", "4444"), application)
    server.serve_forever()
    
四、非开发模式
        - 需要布置静态文件服务器（如：Nginx），负责 /static/ 路由请求
        - 其他请求，靠uwsgi、gevent-server等应用服务器来实现
"""

def product():
    ip = '0.0.0.0'
    port = 4444
    server = WSGIServer((ip, port), application)
    server.serve_forever()


from django.contrib.staticfiles.management.commands.runserver import Command as DebugServer
# from django.core.management.commands.runserver import BaseRunserverCommand

def development():
    # server = BaseRunserverCommand()
    # server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)
    server = DebugServer()
    server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)



if os.environ.get("DEBUG") and os.environ.get("DEBUG_SERVER"):
    main = development
else:
    main = product

logger.info(">>>>>>>>> RUN MODE >>>>>>>>>>>>：%s" %str(main.__name__))
logger.info(">>>>>>>>> patch_status >>>>>>>>>>>>：%s" %str(patch_status))

if __name__ == '__main__':
    # main()
    development()