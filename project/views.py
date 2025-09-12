from django.shortcuts import render,redirect
import cv2
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import base64
from django.contrib import messages
from project.models import student
import os


# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def take_att(request):
    processed_image = None

    if request.method == 'POST' and request.FILES.get('myfile'):
        uploaded_file = request.FILES['myfile']

        # Step 1: Convert uploaded file bytes to OpenCV image
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if frame is None:
            messages.error(request, "Invalid image file!")
            return render(request, 'take_att.html')

        # Step 2: Process image (Face Detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            messages.error(request, "Can't recognize any faces!")
            return render(request, 'take_att.html')

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Step 3: Encode image to Base64 for displaying in HTML
        _, buffer = cv2.imencode('.jpg', frame)
        processed_image = base64.b64encode(buffer).decode('utf-8')
        return render(request, 'take_att.html', {'img': processed_image,'file':uploaded_file})

    return render(request, 'take_att.html')


def gen_frames():
    camera = cv2.VideoCapture(0)  # 0 = default webcam
    while True:
        success, frame = camera.read()
        flip_cam=cv2.flip(frame,1)  #flip vertically
        
        if not success:
            break
        else:
            gray = cv2.cvtColor(flip_cam, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(flip_cam, (x, y), (x+w, y+h), (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', flip_cam)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request,'home.html')

def new_classdb(request):
    images = []
    if request.method == 'POST':
        messages.success(request, "New Data Saved")

        Class = request.POST.get('class')   # use .get() for safety
        uploaded_files = request.FILES.getlist('myfile')  # list of uploaded files

        for f in uploaded_files:
            # Check if already exists
            if student.objects.filter(Photo=f).exists():
                continue
            else:
                # Extract name from filename (before first "_")
                string = str(f).split('_')
                name = string[0]

                rec = student(Class=Class, Name=name, Photo=f)
                rec.save()

        images = student.objects.all()
        return render(request, 'registered_stu.html', {"images": images})

    # Default GET request
    return render(request, 'new_classdb.html')

def deleterow(request):
    stu_id=request.POST.get('stu_id')
    rec=student.objects.get(id=stu_id)
    rec.delete()
    images = student.objects.all()
    return render(request, 'registered_stu.html',{"images": images,'id':stu_id})

def register_student(request):
    return render(request,'register_student.html')

def today_att(request):
    return render(request,'today_att.html')