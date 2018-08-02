import numpy
import cv2
import csv
import dlib
import urllib
import time
from threading import Thread
import requests
import json


def face_detect(img):
    dets = detector(img, 0)
    user_names = []
    unknown_count = 1

    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor = numpy.asarray(list(facerec.compute_face_descriptor(img, shape)), dtype='float32')

        val = 0.5
        user_name = ''

        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                j = numpy.asarray(row['descriptor'].split('\n'), dtype='float32')
                label = row['user_name']

                dist = numpy.linalg.norm(face_descriptor - j)
                if dist < val:
                    val = dist
                    user_name = label

        # If user is exist
        if user_name != '':
            user_names.append(user_name)
        else:
            user_name = "UNKNOWN"
            user_names.append("UNKNOWN " + str(unknown_count))
            unknown_count += 1

    return user_names


def handle_frame(url, cam_key):
    # Use urllib to get the image from the IP camera
    imgResp = urllib.urlopen(url)

    # Numpy to convert into a array
    imgNp = numpy.array(bytearray(imgResp.read()), dtype=numpy.uint8)
    # Finally decode the array to OpenCV usable format ;)
    img = cv2.imdecode(imgNp, -1)

    # To give the processor some less stress
    time.sleep(0.2)
    time.ctime()  # 'Mon Oct 18 13:35:29 2010'
    message = ''
    user_names = face_detect(img)
    if cam_key == 1:
        global frame_num1
        message = time.strftime('%l:%M:%S%p %Z on %b %d, %Y') + ': Camera 1: Frame ' + str(frame_num1) + ': ' + str(user_names)
        frame_num1 += 1
    elif cam_key == 2:
        global frame_num2
        message = time.strftime('%l:%M:%S%p %Z on %b %d, %Y') + ': Camera 2: Frame ' + str(frame_num2) + ': ' + str(user_names)
        frame_num2 += 1
    url = 'http://localhost:5000/api/camera'
    payload = {
        'status': message,
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.status_code, r.reason)


predictor_path = '/home/elsayed/zyama/shape_predictor_68_face_landmarks.dat'
face_rec_model_path = '/home/elsayed/zyama/dlib_face_recognition_resnet_model_v1.dat'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

csv_path = '/home/elsayed/zyama/users_descriptors.csv'

frame_num1 = 1
frame_num2 = 1

# Replace the URL with your own IPwebcam shot.jpg IP:port
url1 = 'http://192.168.1.3:8080/shot.jpg'
url2 = 'http://192.168.1.3:8080/shot.jpg'

while True:
    Thread(target=handle_frame(url1, 1)).start()
    Thread(target=handle_frame(url2, 2)).start()

