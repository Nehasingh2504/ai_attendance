from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import base64
from django.contrib import messages
from home.models import student
import os
import face_recognition
import pickle
from face_recognition import compare_faces, face_distance
 
# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def take_att(request):
    processed_image = None

    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']
        '''stu_Class = request.POST.get('stu_class')

        if stu_Class == 'select':
            messages.error(request, "Select Class")
            return render(request, 'take_att.html')

        # Convert uploaded image bytes to OpenCV
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            messages.error(request, "Invalid image file!")
            return render(request, 'take_att.html')

        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Correct face detection
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            messages.error(request, "Can't recognize any faces!")
            return render(request, 'take_att.html')

        # Draw rectangles correctly
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', frame)
        processed_image = base64.b64encode(buffer).decode('utf-8')

        # face encodings
        file = open(f'media/encodes/class_{stu_Class}','rb')
        known_encodings = pickle.load(file)
        file.close()
        
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        recognized_names = []
        THRESHOLD = 0.45   # start here, tune between ~0.35-0.6

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            if len(known_encodings) == 0:
                name = "Unknown"
            else:
                distances = face_recognition.face_distance(known_encodings, face_encoding)  # numpy array
                best_index = np.argmin(distances)
                best_distance = float(distances[best_index])

                if best_distance <= THRESHOLD:
                    name = best_index
                else:
                    name = "Unknown"

            recognized_names.append(name)'''
        # Load known encodings
        with open("C:/Users/PC/Desktop/CS/ai attendance/project/media/encodes/class_1", "rb") as f:
            known_encodings = pickle.load(f)

        # Read and convert uploaded image
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Encode uploaded image
        unknown_encodings = face_recognition.face_encodings(img)
        if len(unknown_encodings) == 0:
            return "No face detected"

        unknown_encoding = unknown_encodings[0]

        # Compare
        matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.45)
        face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name =  best_match_index
        else:
            name = "Unknown"

        return render(request, 'take_att.html', {'img': processed_image,'faces':uploaded_file,'match':name})

    return render(request, 'take_att.html')
 
def gen_frames():
    camera = cv2.VideoCapture(0)  # 0 = default webcam

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.resize(frame, (600, 380))
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield ( b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request,'home.html')

def student_db(f,stu_Class,encodedlist):
    # Extract name from filename (before first "_")
    string = str(f).split('_')
    name = string[0]
    rec = student(Class=stu_Class, Name=name, Photo=f)
    rec.save()

    images = student.objects.filter(Class = stu_Class)
    unknown_image_url = images[len(images)-1].Photo.path
    unknown_image = face_recognition.load_image_file(unknown_image_url)

    #rgb_frame = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    path=f"media/encodes/class_{stu_Class}"
    if os.path.exists(path):
        file = open(f'media/encodes/class_{stu_Class}','rb')
        known_encodings = pickle.load(file)
        file.close()
        
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        for face_encoding in face_encodings:
            results = compare_faces(known_encodings, face_encoding)
            distances = face_distance(known_encodings, face_encoding)
            best_match_index = distances.argmin()  # smallest distance = most similar face
            name = 'unknown'

        if results[best_match_index]:
            name = best_match_index

        if type(name) != str:
            img_id = images[len(images)-1].id
            images =student.objects.get(id=img_id)
            images.delete()
            return encodedlist

    encodedlist.append(unknown_encoding)

    return encodedlist

def new_classdb(request):      # to delete all data in database 'python manage.py flush'
    images = []
    if request.method == 'POST':
        stu_Class=request.POST.get('class')   # use .get() for safety
        uploaded_files = request.FILES.getlist('myfile')  # list of uploaded files
        encodedlist=[]

        for f in uploaded_files:
            encodedlist=student_db(f,stu_Class,encodedlist)
        
        if len(encodedlist)!=0:
            os.makedirs('media/encodes', exist_ok=True)  # Create folders if not exist
            file = open(f"media/encodes/class_{stu_Class}", 'wb')
            pickle.dump(encodedlist, file)
            file.close()

        images = student.objects.filter(Class = stu_Class)
        return render(request, 'registered_stu.html', {"images": images})

    return render(request, 'new_classdb.html')

def deleterow(request):
    stu_id=request.POST.get('stu_id')
    stu_class=request.POST.get('class')
    rec=student.objects.get(id=stu_id)
    rec.delete()
    images = student.objects.filter(Class = stu_class)
    return render(request, 'registered_stu.html',{"images": images,'id':stu_class})

def registered_stu(request):
    stu_Class = request.POST.get('btn')
    all_student = student.objects.filter(Class = stu_Class)
    return render(request,'registered_stu.html',{'images': all_student})

def today_att(request):
    return render(request,'today_att.html')

def register_stuform(request):
    return render(request,'register_stuform.html')

def detect_stu(request):
    file = cv2.imread('project/student/class_1')
    if file is None:
        print('success')

    else:
        print('error')