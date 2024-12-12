FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /usr/src/app/settings
COPY *.py /usr/src/app
RUN mkdir -p /usr/src/app/.lgd-nfy0 && chown -R 1000:1000 /usr/src/app/.lgd-nfy0

CMD [ "python", "/usr/src/app/main.py" ]