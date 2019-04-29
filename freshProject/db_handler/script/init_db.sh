#!/usr/bin/env bash
#"""
#测试的数据脚本一概放入DEBUG里面
#"""


# 第一次创建makemigrations时需要带上app name
python manage.py makemigrations

#python manage.py migrate    --noinput
python manage.py migrate


if [ "$DEBUG" == "True" ]; then
    echo "use debug mode"
#    python manage.py loaddata ppermission_config_init.json

else
    echo "use product mode"

fi



exec "$@"