# source_user/Dockerfile

FROM python:3.9-alpine

RUN pip install pymongo==3.11.3 flask

WORKDIR /

COPY data_user.py .
COPY app.py .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

