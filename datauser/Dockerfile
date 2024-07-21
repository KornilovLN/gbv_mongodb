# datauer/Dockerfile

FROM python:3.9-alpine

WORKDIR /

COPY data_user.py /

RUN pip install pymongo==3.11.3

CMD ["python", "/data_user.py"]
