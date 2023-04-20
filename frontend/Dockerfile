FROM python:3.9.5-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /frontend

RUN mkdir /frontend/static

RUN mkdir /frontend/templates

WORKDIR /frontend

COPY cert.pem /frontend/

COPY key.pem /frontend/

COPY static/ /frontend/static/

COPY templates/ /frontend/templates/

COPY frontend.py /frontend/

#COPY wsgi.py /frontend/

RUN python3 -m pip install --upgrade pip

COPY requirements.txt /frontend/

RUN pip3 install -r /frontend/requirements.txt

RUN pip3 install gunicorn

EXPOSE 5501

#CMD [ "python3", "frontend.py"]

CMD [ "gunicorn", "--certfile", "cert.pem", "--keyfile", "key.pem", "-w", "4", "--bind", "0.0.0.0:5501", "frontend:app", "--access-logfile", "'-'"]