import numpy
import cv2
import csv
import dlib


def face_detect(img):
    dets = detector(img, 0)

    if len(dets) == 0:
        print('Sorry I can\'t find any face in this picture.')
    else:
        print('I have found ' + str(len(dets)) + ' face/s in this picture.')
        print('Press \'q\' to close the window.')

    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor1 = facerec.compute_face_descriptor(img, shape)
        face_descriptor2 = numpy.asarray(list(face_descriptor1), dtype='float32')

        val = 0.5
        user_name = ''

        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                j = numpy.asarray(row['descriptor'].split('\n'), dtype='float32')
                label = row['user_name']

                dist = numpy.linalg.norm(face_descriptor2 - j)
                # print(dist)
                if dist < val:
                    val = dist
                    user_name = label

        # If user is exist
        if user_name != '':
            cv2.imshow('frame', img)
            cv2.waitKey(0)
            print("Sorry I know this person before .. this is " + user_name + '.')
            print('Please try again with another person.')
        else:
            cv2.imshow('frame', img)
            cv2.waitKey(0)
            print('Well, I don\'t know this person.')
            user_name = raw_input('Can you tell me his/her name: ')

            with open(csv_path, 'a') as o:
                fieldnames = ['user_name', 'descriptor']
                writer = csv.DictWriter(o, fieldnames=fieldnames)
                writer.writerow({'user_name': user_name, 'descriptor': face_descriptor1})

            print('The user was added successfully.')


cap = cv2.VideoCapture(0)
predictor_path = '/home/elsayed/zyama/shape_predictor_68_face_landmarks.dat'
face_rec_model_path = '/home/elsayed/zyama/dlib_face_recognition_resnet_model_v1.dat'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
csv_path = '/home/elsayed/zyama/users_descriptors.csv'

print("I can help you to add users to your database.")

frame_num = 1
print('I will take a shot after')
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:

        if frame_num == 8:
            face_detect(frame)
            break
        elif frame_num == 2:
            print(3)
        elif frame_num == 4:
            print(2)
        elif frame_num == 6:
            print(1)
            print('NOW')
        frame_num += 1

cap.release()
cv2.destroyAllWindows()
