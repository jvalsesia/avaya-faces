python -m venv venv

. venv/Scripts/activate

venv/Scripts/python -m pip install --upgrade pip

venv/Scripts/pip install flask

venv/Scripts/pip freeze > requirements.txt

venv/Scripts/pip install -r requirements.txt

venv/Scripts/pip install gunicorn

venv/bin/gunicorn --certifile cert.pen --keyfile key.pem --bind 0.0.0.0:5501 wsgi:app
