# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
from gevent import monkey
import os

def log_setup(progname, add_logger_name=True):
    syslogfmt = progname + '[%%(process)d]: [%%(levelname)s] %s%%(message)s' % (
    '%(name)s - ' if add_logger_name else '')
    config = lambda x: logging.basicConfig(level=x, format='%(asctime)s ' + syslogfmt)
    # if args.log_config:
    #     logging.config.fileConfig(args.log_config)

    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    config(log_level)

    logger = logging.getLogger(__name__)

    logger.info('The log level is %s' % log_level)


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

log_setup(PROGRAM)

"""
先搞清 WSGI application(handler)  /  WSGI Server 的区别与联系
    - WSGI Server负责获取http请求，将请求传递给WSGI application，由application处理请求后返回response
    
django WSGIServer的位置：
    - from django.core.servers.basehttp import run, WSGIServer

一、 django-runserver的部分实现(基类)
        - 实现了AutoReload机制（可设置）
        - 不包含静态文件的处理handler（WSGI application）
        - 可处理普通接口，不支持静态文件/static/路径访问

    from django.core.management.commands.runserver import BaseRunserverCommand

    server = BaseRunserverCommand()
    server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)


二、django-runserver的完全实现
        - 实现了AutoReload机制（可设置）
        - 并且添加了StaticFilesHandler的静态文件的处理handler
        - StaticFilesHandler继承自基本的WSGIhandler（WSGI application），实现接口请求响应，并添加了静态文件的处理
        - 当服务器启动，等于 Python manage.py runserver

    from django.contrib.staticfiles.management.commands.runserver import Command as DebugServer
    server = DebugServer()
    server.handle(use_ipv6=False, addrport="0.0.0.0:4444", use_reloader=True, use_threading=False)

三、gevent的WSGIServer的实现
        - 协程异步接口实现
        - 普通WSGI协议实现，不调用静态文件处理handler
        
    from gevent.pywsgi import WSGIServer
    from freshProject.wsgi import application

    server = WSGIServer(("0.0.0.0", "4444"), application)
    server.serve_forever()
    
四、非开发模式
        - 需要布置静态文件服务器（如：Nginx），负责 /static/ 路由请求
        - 其他请求，靠uwsgi、gevent-server等应用服务器来实现
"""

# ip = 'localhost'
ip = '0.0.0.0'
port = 4444

def product():
    server = WSGIServer((ip, port), application)
    logger.info('Running PRODUCT on http://%s:%d/' % (ip, port))
    server.serve_forever()

# from django.core.wsgi import WSGIHandler
from django.contrib.staticfiles.management.commands.runserver import Command
# from django.core.management.commands.runserver import BaseRunserverCommand

def development():
    # server = BaseRunserverCommand()
    server = Command()
    logger.info('Running DEBUG on http://%s:%d/' % (ip, port))
    server.handle(use_ipv6=False, addrport="%s:%s"%(ip, port),
                  use_reloader=True, use_threading=True,
                  use_static_handler=True, insecure_serving=True)


if os.environ.get("DEBUG") and os.environ.get("DEBUG_SERVER"):
    main = development
else:
    main = product

logger.info(">>>>>>>>> RUN MODE >>>>>>>>>>>>：%s" %str(main.__name__))
logger.info(">>>>>>>>> patch_status >>>>>>>>>>>>：%s" %str(patch_status))


if __name__ == '__main__':
    # main()
    development()