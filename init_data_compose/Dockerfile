FROM python:3.6

COPY ../db_handler /work

WORKDIR /work

RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/

ENTRYPOINT ["/work/script/init_db.sh"]

RUN cd ..

CMD ["python", "manage.py", "makemigrations"]
