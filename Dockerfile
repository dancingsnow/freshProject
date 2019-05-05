FROM python:3.6

ARG BUILD_VERSION=1.0.0

COPY .. /work

WORKDIR /work

VOLUME /www/fresh

RUN echo "VERSION='${BUILD_VERSION}'" > /work/freshProject/freshProject/__init__.py

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

RUN python setup.py install

RUN cp prod_entrypoint.sh /usr/bin/ && chmod +x /usr/bin/prod_entrypoint.sh

EXPOSE 8888

ENTRYPOINT ["prod_entrypoint.sh"]

CMD ["fresh-server-start"]