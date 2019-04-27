#!/usr/bin/env bash

cd /work
#pip install -r requirements.txt -i https://pypi.douban.com/simple

if [ "$DEBUG" == "true" ]; then
    echo "use debug mode"
    python setup.py develop
    db-manage makemigrations
    db-manage migrate
else
    echo "use product mode"
	python setup.py install

fi

python setup.py install

exec "$@"