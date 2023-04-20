# 1- Build

## Ubuntu
```bash
sudo apt install cmake gcc g++ python-dev python-numpy python3-dev python3-numpy libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgtk2.0-dev libgtk-3-dev libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev
```

## Fedora
```bash
sudo dnf install cmake python-devel numpy gcc gcc-c++ gtk2-devel libdc1394-devel ffmpeg-devel gstreamer-plugins-base-devel libpng-devel libjpeg-turbo-devel jasper-devel openexr-devel libtiff-devel libwebp-devel tbb-devel eigen3-devel
```

## docker-compose
```bash
docker-compose up -d
```


# Configure and Test Mongo Database Container
The **docker-compose.yml** contains the Mongo Database credentials.

Attach shell to Mongo:
```bash
docker exec -it mongodb bash
```

Connect to mongo, check the mongodb environment properties.
```
MONGO_INITDB_ROOT_USERNAME: root
MONGO_INITDB_ROOT_PASSWORD: Avaya123!
```

```bash
mongo -u root -p
```

Change to database:
```bash
use facesdb
```


Create application's database user used for avayafaces-api:
```bash
db.createUser({user: 'apiuser', pwd: 'api123!', roles: [{role: 'readWrite', db: 'facesdb'}]})
```

Show tables:
```bash
show tables
```

List collections:
```bash
db.user_enrollments.find()
```

Delete all documents in collections:
```bash
db.user_enrollments.deleteMany({})
```

Delete one document in collections:
```bash
db.user_enrollments.deleteOne({ username: "jvalsesia"})
```

Exit from Mongo: 
```bash
exit
```

Check the Credentials:
```bash
mongo -u apiuser -p api123! --authenticationDatabase facesdb
```

# Prod
```bash
docker login -u avaya -p Avaya@123 dockerregistry.ept-solutions.com
docker-compose -f docker-compose.yml up -d
```

# References
## Virtual Evironment (venv)
The **venv** module provides support for creating lightweight "*virtual environments*" with their own site directories, optionally isolated from system site directories. Each virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories.

## SSL
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

## HTML5 Canvas and Video
https://medium.com/yemeksepeti-teknoloji/using-html5-video-with-canvas-acb1ba8f6441

## Flask 2 Rest API
https://www.youtube.com/watch?v=Hti3LCocY8k
https://www.youtube.com/watch?v=lI220GRfCZ0


## Base64 Image Python
https://medium.com/swlh/restful-image-transfer-with-base64-encoding-cd9fb4453598
https://morioh.com/p/11156fb8e37e

## Flack-PyMongo
https://flask-pymongo.readthedocs.io/en/latest/

## Mongo commands
https://www.shellhacks.com/mongodb-show-collection-data-mongo-shell/


## Download socket.io
```bash
curl -k https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js --output socket.io.js
```
