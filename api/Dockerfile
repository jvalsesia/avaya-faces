FROM python:3.9.5-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -y build-essential cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

RUN mkdir /api

WORKDIR /api

COPY cert.pem /api/

COPY key.pem /api/

COPY requirements.txt /api/

COPY api.py /api/

#COPY wsgi.py /api/

RUN python -m pip install --upgrade pip

RUN pip3 install -r /api/requirements.txt

RUN pip3 install eventlet==0.30.2

RUN pip3 install gunicorn

EXPOSE 5500

#CMD [ "python3", "api.py"]
CMD [ "gunicorn", "--certfile", "cert.pem", "--keyfile", "key.pem", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5500", "api:app", "--access-logfile", "-", "--log-level", "debug"]