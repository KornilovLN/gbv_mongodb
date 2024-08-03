#--- Сначала создайте файл Dockerfile с содержимым:
#--- docker build -t clear_database .
#--- Чтобы очистить базу данных, нужно запустить контейнер с помощью команды:
#--- docker run --rm --network net_gen_db clear_database
#--- Не забудьте указать сеть, в которой будет запущен контейнер.
#--- А перед этим stop контейнерам data_generator и data_user.
#--- и потом запустить их снова после очистки базы.

FROM python:3.9-alpine

RUN pip install pymongo

COPY clear_database.py /clear_database.py

CMD ["python", "/clear_database.py"]
