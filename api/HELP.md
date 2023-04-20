https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html


# Ubuntu
```bash
sudo apt install cmake gcc g++ python-dev python-numpy python3-dev python3-numpy libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgtk2.0-dev libgtk-3-dev libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev
```

# Fedora
```bash
sudo dnf install cmake python-devel numpy gcc gcc-c++ gtk2-devel libdc1394-devel ffmpeg-devel gstreamer-plugins-base-devel libpng-devel libjpeg-turbo-devel jasper-devel openexr-devel libtiff-devel libwebp-devel tbb-devel eigen3-devel
```


# Virtual Enviroment
python -m venv venv

. venv/bin/activate

venv/bin/python -m pip install --upgrade pip

venv/bin/pip install wheel cmake

venv/bin/pip install flask flask_restful flask_cors flask_socketio

venv/bin/pip install mongoengine

venv/bin/pip install opencv-python face_recognition

venv/bin/pip install gunicorn

venv/bin/pip freeze > requirements.txt

pip install -r requirements.txt

venv/bin/gunicorn --certifile cert.pen --keyfile key.pem --bind 0.0.0.0:5500 wsgi:app
