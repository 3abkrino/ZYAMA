import numpy
import cv2
import csv
import dlib


def face_detect(img):
    dets = detector(img, 0)
    user_names = []
    unknown_count = 1

    for k, d in enumerate(dets):
        is_face = True
        shape = sp(img, d)
        face_descriptor = numpy.asarray(list(facerec.compute_face_descriptor(img, shape)), dtype='float32')
        cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
        width = d.right() - d.left()
        val = 0.5
        user_name = ''

        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                j = numpy.asarray(row['descriptor'].split('\n'), dtype='float32')
                label = row['user_name']

                dist = numpy.linalg.norm(face_descriptor - j)
                # print(dist)
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
            '''
            with open('/home/elsayed/zyama/users_descriptors.csv', 'a') as o:
                fieldnames = ['user_name', 'descriptor']
                writer = csv.DictWriter(o, fieldnames=fieldnames)
                writer.writerow({'user_name': user_name, 'descriptor': face_descriptor})
            '''
        cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
        cv2.rectangle(img, (d.left() - 2, d.top() - 50), (d.right() + 2, d.top()), (0, 255, 0),
                      cv2.FILLED)

        user_name_len = len(user_name)
        font_size = float(width / user_name_len / 2)
        cv2.putText(img, user_name,
                    (d.left() + 10, d.top() - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_size/10, (255, 0, 0))

    return user_names, img


cap = cv2.VideoCapture(0)
predictor_path = '/home/elsayed/zyama/shape_predictor_68_face_landmarks.dat'
face_rec_model_path = '/home/elsayed/zyama/dlib_face_recognition_resnet_model_v1.dat'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

csv_path = '/home/elsayed/zyama/users_descriptors.csv'

frame_num = 1
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # cv2.imshow('frame', frame)
        if frame_num % 4 == 0:
            user_names, img = face_detect(frame)
            cv2.imshow('frame', img)
            print(str(frame_num) + ': ' + str(user_names))
        frame_num += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
