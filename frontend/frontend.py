
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)


@app.route('/haarcascade_frontalface_alt2.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def index_form():
    return render_template('index.html')

@app.route('/recognition')
def schedule_form():
    return render_template('recognition.html')

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5501, debug=False, threaded=True)

