import face_recognition
import os 
import pickle
import cv2
known_encodings=[]
path = 'C:/Users/PC/Desktop/CS/ai attendance/project/student/class_1'
for filename in os.listdir(path):
    print(filename)
    img_path = os.path.join(path, filename)
    known_image = face_recognition.load_image_file(img_path)
    known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    known_encodings.append(known_encoding)

'''file = open(f'C:/Users/PC/Desktop/CS/ai attendance/project/media/encodes/class_1','rb')
known_encodings = pickle.load(file)
file.close()'''
# Load unknown image (to check)
unknown_image = face_recognition.load_image_file("C:/Users/PC/Desktop/CS/ai attendance/project/student/class_2/Liam_2.jpeg")
unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
# Find all faces and encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
 
# Compare with known encodings
from face_recognition import compare_faces, face_distance

for face_encoding in face_encodings:
    results = compare_faces(known_encodings, face_encoding)
    distances = face_distance(known_encodings, face_encoding)
    best_match_index = distances.argmin()  # smallest distance = most similar face

    name = 'unknown'
    if results[best_match_index]:
        name = best_match_index

print(f"Detected: {name}")
if type(name) != str:
    print('match')
