# datauer/Dockerfile

FROM python:3.9-alpine

RUN pip install pymongo==3.11.3

WORKDIR /

COPY data_user.py /



CMD ["python", "/data_user.py"]
