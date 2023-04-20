let face;
let thickness = 2;

function openCvReady() {
    cv['onRuntimeInitialized'] = () => {
        let video = document.getElementById("cam_input"); // video is the id of video tag
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (err) {
                console.log("An error occurred! " + err);
            });
        let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
        let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
        let gray = new cv.Mat();
        let cap = new cv.VideoCapture(cam_input);
        let faces = new cv.RectVector();
        let classifier = new cv.CascadeClassifier();
        let utils = new Utils('errorMessage');
        let faceCascadeFile = 'haarcascade_frontalface_alt2.xml'; // path to xml
        utils.createFileFromUrl(faceCascadeFile, faceCascadeFile, () => {
            classifier.load(faceCascadeFile); // in the callback, load the cascade from file 
        });
        const FPS = 24;
        const acceptableWidth = 150;
        const messagePoint = new cv.Point(10,50);
        function processVideo() {
            let begin = Date.now();
            cap.read(src);
            src.copyTo(dst);
            cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
            try {
                classifier.detectMultiScale(gray, faces, 1.1, 3, 0);
                //console.log(faces.size());
            } catch (err) {
                console.log(err);
            }
            let color = [0, 255, 0, 255]

            for (let i = 0; i < faces.size(); ++i) {
                face = faces.get(i);
                let point1 = new cv.Point(face.x, face.y);
                let point2 = new cv.Point(face.x + face.width, face.y + face.height);

                if (face.width < acceptableWidth - 5) {
                    color = [255, 0, 0, 255]
                    // cv.putText(dst, "Too Far " + face.width, point1, cv.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness);
                    cv.putText(dst, "Too far. Please come closer. " , messagePoint, cv.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness);
                } else if (face.width > (acceptableWidth * 1.5)) {
                    color = [0, 0, 255, 255]
                    cv.putText(dst, "Face is too close. Please move back. ", messagePoint, cv.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness);
                } else {
                    color = [0, 255, 0, 255]
                    cv.putText(dst, "Perfect. Please stand still.", messagePoint, cv.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness);
                }
                cv.rectangle(dst, point1, point2, color, thickness);
            }
            cv.imshow("canvas_output", dst);
            // schedule next one.
            let delay = 1000 / FPS - (Date.now() - begin);
            setTimeout(processVideo, delay);
        }
        // schedule first one.
        setTimeout(processVideo, 0);
    };
}




function takeImageShot() {
    if(document.getElementById("recognized_userName") != null) {
        document.getElementById("recognized_userName").innerHTML = "";
    }
 
    if (face != null) {
        let canvas = document.getElementById("canvas_output");
        let ctx = canvas.getContext('2d');
        let faceImage = ctx.getImageData(face.x + thickness, face.y + thickness, face.width - thickness, face.height - thickness);

        // destination canvas
        canvas = document.getElementById("image_shot");
        ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width = faceImage.width;
        canvas.height = faceImage.height;
        ctx.putImageData(faceImage, 0, 0);
    }
}


