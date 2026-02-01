const express = require('express');
const fs = require("fs");
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const app = express();
const upload = require('./upload')
const cors = require("cors");

// Middleware
app.use(cors()); // allow frontend requests
app.use(express.json()); // parse JSON body
app.use(express.static('public'));
app.use('/student_img', express.static('student_img'))
app.use(express.urlencoded({ extended: true }))

// Open DB once at startup
const db = new sqlite3.Database('./attendance.db');

// Create table if not exists
db.run(`
  CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    date TEXT,
    time TEXT
  )
`);

// Route: receive data from frontend & send response back
app.post("/api/data", (req, res) => {
  const { selectedClass } = req.body;
  const folderPath = path.join(__dirname, "public", "known_faces", `class_${selectedClass}`);
  console.log("Received from frontend:", selectedClass);
  fs.readdir(folderPath, (err, files) => {
    if (err) {
      return res.status(500).json({ error: "Unable to read folder" });
    }
    res.json(files); // send file names to frontend
  });
});

// Route to mark attendance
app.post('/attendance', (req, res) => {
  const { studentId } = req.body;

  db.get(
    `SELECT * FROM attendance WHERE student_id = ? AND date = DATE('now')`,
    [studentId],
    (err, row) => {
      if (err) return res.status(500).json({ error: err.message });

      if (row) {
        return res.json({ message: 'Already marked' });
      }

      db.run(
        `INSERT INTO attendance (student_id, date, time)
         VALUES (?, DATE('now'), TIME('now'))`,
        [studentId],
        (err) => {
          if (err) return res.status(500).json({ error: err.message });
          res.json({ message: 'Attendance marked' });
        }
      );
    }
  );
});

app.post('/submit-form', upload.array('myfile'), (req, res) => {
  console.log(req.body)
  const stuclass = req.body.class
  const files = req.files   // REAL uploaded files
  console.log(files)
  const db = new sqlite3.Database(`attendance/class${stuclass}_attendance.db`)
  const stu_img_db = new sqlite3.Database(`student_img_db/class${stuclass}_stus.db`)

  let days = ""
  for (let i = 1; i <= 31; i++) {
    days += `day${i} INTEGER DEFAULT 0, `
  }
  days = days.slice(0, -2)

  // Attendance table
  db.run(`
    CREATE TABLE IF NOT EXISTS class${stuclass}_attendance (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      student_name TEXT UNIQUE,
      ${days}
    )
  `)

  // Image table (student_name UNIQUE)
  stu_img_db.run(`
    CREATE TABLE IF NOT EXISTS class${stuclass}_stus (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      student_name TEXT UNIQUE,
      image_path TEXT
    )
  `)

  files.forEach(file => {
    const studentName = file.originalname.split('_')[0]
    const imagePath = file.path.replace(/\\/g, '/')
    console.log(studentName)
    // CHECK DUPLICATE
    stu_img_db.get(
      `SELECT id FROM class${stuclass}_stus WHERE student_name = ?`,
      [studentName],
      (err, row) => {
        if (row) {
          return
        }

        // INSERT ATTENDANCE (safe due to UNIQUE)
        db.run(
          `INSERT OR IGNORE INTO class${stuclass}_attendance (student_name)
       VALUES (?)`,
          [studentName]
        )

        // INSERT IMAGE RECORD
        stu_img_db.run(
          `INSERT INTO class${stuclass}_stus (student_name, image_path)
       VALUES (?, ?)`,
          [studentName, imagePath]
        )
      }
    )
  })
  db.close()
  stu_img_db.close()
  res.redirect(`/registered_stu.html?class=${stuclass}`)
})

app.get('/get-table/:class', (req, res) => {
  const stuclass = req.params.class
  console.log('class', stuclass)
  const stu_img_db = new sqlite3.Database(`student_img_db/class${stuclass}_stus.db`)
  stu_img_db.all(`SELECT * FROM class${stuclass}_stus`, (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message })
    }
    res.json(rows)
  }
  )
})

app.post('/deleterow', (req,res) => {
  const stuclass = req.body.class
  const stuid = req.body.stu_id
  console.log('click',stuclass,stuid)
  const stu_img_db = new sqlite3.Database(`student_img_db/class${stuclass}_stus.db`)
  const attDB = new sqlite3.Database(`attendance/class${stuclass}_attendance.db`)
  stu_img_db.get(`SELECT id FROM class${stuclass}_stus WHERE id = ?`,stuid,(err,rows)=>{
    if (err) {
      return res.status(500).json({ error: err.message })
    }
    else if(rows){
      // Delete image file
      if (fs.existsSync(imagePath)) {
        fs.unlinkSync(imagePath)
      }

      // Delete from image table
      imgDB.run(
        `DELETE FROM class${stuclass}_stus WHERE id = ?`,
        [stuid]
      )

      // Delete from attendance table (by student_name)
      attDB.run(
        `DELETE FROM class${stuclass}_attendance WHERE student_name = ?`,
        [row.student_name]
      )

      // Delete from attendance table (by student_name)
      stu_img_db.run(
        `DELETE FROM class${stuclass}_stus WHERE id = ?`,
        [stuid]
      )
      res.redirect(`/registered_stu.html?class=${stuclass}`)
    }
  })
})
app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
