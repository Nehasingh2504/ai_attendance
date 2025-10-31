# AI Attendance System

> **Smart, real-time attendance using face recognition and image upload**

---

## 🔎 Project Overview

An **AI-powered Attendance Management System** built using **Django**, **OpenCV**, and modern front-end tools (**HTML**, **CSS**, **JavaScript**). The system supports both **real-time face detection** via webcam and **manual photo uploads** to mark attendance. It also allows creating **separate databases for each class**, maintaining student details and attendance records independently.

Perfect for schools, colleges, and offices looking for a simple, smart, and automated attendance solution.

---

## 🚀 Features

✅ Real-time face detection and recognition using OpenCV
✅ Option to upload student images for attendance marking
✅ Create and manage multiple classes (each with its own database)
✅ Store student details, attendance records, and class info separately
✅ Responsive and easy-to-use web interface
✅ Attendance dashboard with daily and overall summaries

---

## 🧩 Tech Stack

* **Backend:** Django
* **Computer Vision:** OpenCV (face detection and recognition)
* **Frontend:** HTML5, CSS3, JavaScript
* **Database:** SQLite (per-class database creation)

---

## 📸 Preview
###  Dashboard
![dashboard](https://github.com/user-attachments/assets/e0087911-ee17-48cb-ad01-cc050ffd1f1c)

###  Student Profile
![student profile](https://github.com/user-attachments/assets/402d6b09-3f3d-401a-a064-a7c63d188201)

### Registration Form
![student profile](https://github.com/user-attachments/assets/3ee85849-0b2a-4b58-abb7-daeec4856ac6)

### Attendance Detail
![Attendance](https://github.com/user-attachments/assets/7034e180-46b8-4f48-9d9b-546ad484c729)

### AI Attendance
![Attendance](https://github.com/user-attachments/assets/f3685212-6e7a-472a-8e5d-d8927b504be5)

---

<!-----

## 📁 Project Structure

```
ai-attendance/
├─ attendance/              # Main Django app
│  ├─ migrations/
│  ├─ models.py              # Student, Class, AttendanceRecord
│  ├─ views.py
│  ├─ urls.py
│  ├─ forms.py
│  └─ templates/
│     ├─ index.html
│     ├─ upload.html         # Upload image for attendance
│     └─ dashboard.html
├─ static/
│  ├─ css/
│  ├─ js/
│  └─ images/
├─ database_manager/         # Handles class-specific DB creation
│  ├─ create_db.py
│  ├─ switch_db.py
├─ recognition/              # Face recognition utilities
│  ├─ capture_realtime.py
│  ├─ recognize.py
│  ├─ train.py
│  └─ upload_recognition.py
├─ manage.py
└─ README.md
```-->

---

## 🎥 Real-time Recognition Mode

* System captures video feed from webcam.
* Detects faces using OpenCV.
* Recognizes registered students using trained model.
* Marks attendance instantly in the class database.

### 🖼️ Upload Image Mode

* Instructor uploads student photo manually.
* Backend compares the uploaded image with known embeddings.
* If a match is found, attendance is marked.

### 🗂️ Class & Database Management

* Each new class created has its own SQLite database file.
* Each database stores unique student and attendance records.
* Admins can switch between classes or merge reports.

---

## 🙋 Author & Contact

* **Neha Singh — Developer & Designer**
* 📧 Email: `nehasinghagra0101@gmail.com`
* 💻 GitHub: [NehaSingh2504](https://github.com/Nehasingh2504)
* 🔗 LinkedIn: [Neha Singh](https://www.linkedin.com/in/neha-singh-065245264/)

---

### ⭐ If you like this project, don’t forget to **star the repo** and **contribute!**
