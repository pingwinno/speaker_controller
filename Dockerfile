FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /usr/src/app/settings
COPY *.py /usr/src/app

CMD [ "python", "/usr/src/app/main.py" ]