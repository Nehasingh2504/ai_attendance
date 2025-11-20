import cv2
import face_recognition
import numpy as np
import pickle
import os

def check_face():
    # Load known encodings
    known_encodings = []
    path = 'C:/Users/PC/Desktop/CS/ai attendance/project/student/class_1'

    for filename in os.listdir(path):
        print(filename)
        img_path = os.path.join(path, filename)
        known_image = cv2.imread(img_path)
        known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)

        enc = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(enc)

    # Load unknown
    img_path = os.path.join('C:/Users/PC/Desktop/CS/ai attendance/project/student/class_2', 'Liam_2.jpeg')
    unknown_image = cv2.imread(img_path)
    img = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)

    unknown_locations = face_recognition.face_locations(img)
    unknown_encodings = face_recognition.face_encodings(img, unknown_locations)

    if len(unknown_encodings) == 0:
        print("No face detected")
        return
    
    unknown_encodings = unknown_encodings[0]
    matches = face_recognition.compare_faces(known_encodings, unknown_encodings)
    face_distances = face_recognition.face_distance(known_encodings, unknown_encodings)

    # Find best match index
    best_match_idx = np.argmin(face_distances)
    if matches[best_match_idx]:
        print("Match Found at index:", best_match_idx)
    else:
        print("Unknown")

check_face()
