FROM python:3.6

COPY . /test

WORKDIR /test

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD py.test -s