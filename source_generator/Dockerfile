# datagenerator/Dockerfile

FROM python:3.9-alpine

RUN pip install pymongo

COPY data_generator.py /data_generator.py

CMD ["python", "/data_generator.py"]
