FROM hub.rowenatech.com/build/python-java:2.7-8

ARG BUILD_VERSION=1.0.0

COPY . /work

WORKDIR /work

VOLUME /www/sgcc

RUN echo "VERSION='${BUILD_VERSION}'" > /work/sgcc_server/__init__.py

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

RUN python setup.py install

RUN cp prod_entrypoint.sh /usr/bin/ && chmod +x /usr/bin/prod_entrypoint.sh

EXPOSE 8090

EXPOSE 8888

ENTRYPOINT ["prod_entrypoint.sh"]

CMD ["sgcc-server-start"]