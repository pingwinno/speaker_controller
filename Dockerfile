FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /usr/src/appsettings
COPY *.py /usr/src/app

CMD [ "python", "./main.py" ]