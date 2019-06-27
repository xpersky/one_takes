FROM python:3.6

RUN git clone https://github.com/macloo/basic-flask-app.git ./app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV FLASK_APP routes.py

ENV FLASK_RUN_HOST 0.0.0.0

CMD flask run 


