def take_att(request):
    processed_image = None

    if request.method == 'POST':
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
        return render(request, 'take_att.html', {'img': processed_image,'faces':faces})

    return render(request, 'take_att.html')