const multer = require('multer')
const path = require('path')
const fs = require('fs')

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const stuclass = req.body.class
    const dir = path.join('student_img', `class${stuclass}`)
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
    cb(null, dir)
  },

  filename: (req, file, cb) => {
    const studentName = file.originalname.split('_')[0]
    cb(null, `${studentName}.jpg`) // UNIQUE FILE
  }
})

module.exports = multer({ storage })

/*const multer = require('multer')

const upload = multer({
  storage: multer.memoryStorage()
})
module.exports = upload*/
