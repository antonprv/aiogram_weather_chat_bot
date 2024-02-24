FROM python:3.11.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]

LABEL authors="antonprv"