def student_db(f,stu_Class,Imagepath,count=3):
    # Check if already exists
    if student.objects.filter(Photo=f).exists()==False:
    # Extract name from filename (before first "_")
        string = str(f).split('_')
        name = string[0]
        count=5
        rec = student(Class=stu_Class, Name=name, Photo=f)
        rec.save()
    Imagepath.append(cv2.imread(os.path.abspath(f"media/student/class_{stu_Class}/{f}")))
    return Imagepath,count

def new_classdb(request):      # to delete all data in database 'python manage.py flush'
    images = []
    count=1
    if request.method == 'POST':
        messages.success(request, "New Data Saved")

        stu_Class=request.POST.get('class')   # use .get() for safety
        uploaded_files = request.FILES.getlist('myfile')  # list of uploaded files
        uploaded_single_files = request.POST.get('myfile')
        Imagepath=[]
        if len(uploaded_files)!=0:
            for f in uploaded_files:
                Imagepath,count=student_db(f,stu_Class,Imagepath)
            
        else:
            Imagepath=student_db(uploaded_single_files,stu_Class,Imagepath)

        encodedlist=[]
        for img in Imagepath:
            img =  cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodedlist.append(encode)

        os.makedirs('media/encodes', exist_ok=True)  # Create folders if not exist

        file = open(f"media/encodes/class_{stu_Class}", 'wb')
        pickle.dump(encodedlist, file)
        file.close()

        images = student.objects.filter(Class = stu_Class)
        return render(request, 'registered_stu.html', {"images": images,"class":stu_Class})

    return render(request, 'new_classdb.html')