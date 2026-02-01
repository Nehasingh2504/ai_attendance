const video = document.getElementById('video')

// Start webcam
startVideo()
function startVideo(){
  navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 400 } })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error(err))
}

// Load model
Promise.all([
  faceapi.nets.ssdMobilenetv1.loadFromUri('/models')
]).then(() => console.log('Model loaded'))

video.addEventListener('play', () => {
  const wrapper = document.getElementById('video-wrapper')
  const canvas = faceapi.createCanvasFromMedia(video)
  wrapper.appendChild(canvas)

  canvas.style.position = 'absolute'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.zIndex = '10'

  const displaySize = { width: 640, height: 400 }
  faceapi.matchDimensions(canvas, displaySize)

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video)
    const resizedDetections = faceapi.resizeResults(detections, displaySize)

    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    resizedDetections.forEach(det => {
      const { x, y, width, height } = det.box

      // Green styling
      ctx.strokeStyle = '#00FF00'  // Bright green
      ctx.lineWidth = 4

      // Rounded rectangle
      const radius = 15
      ctx.beginPath()
      ctx.moveTo(x + radius, y)
      ctx.lineTo(x + width - radius, y)
      ctx.quadraticCurveTo(x + width, y, x + width, y + radius)
      ctx.lineTo(x + width, y + height - radius)
      ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height)
      ctx.lineTo(x + radius, y + height)
      ctx.quadraticCurveTo(x, y + height, x, y + height - radius)
      ctx.lineTo(x, y + radius)
      ctx.quadraticCurveTo(x, y, x + radius, y)
      ctx.stroke()
    })
  }, 1000)
})

//face recognition
Promise.all([
  faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/models')
]).then(startVideo)

async function loadKnownFaces(data) {
  const labels = data

  return Promise.all(
    labels.map(async label => {
      const img = await faceapi.fetchImage(`/known_faces/class_1/${label}`)
      const detection = await faceapi
        .detectSingleFace(img)
        .withFaceLandmarks()
        .withFaceDescriptor()
      return new faceapi.LabeledFaceDescriptors(label, [detection.descriptor])
    })
  )
}

video.addEventListener('play', async () => {
  selectedClass = document.getElementById('class_select')
  selectedClass.addEventListener('change', async function () {
    const response = await fetch("http://localhost:3000/api/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selectedClass: selectedClass.value })
    });
    const data = await response.json();

    const knownFaces = await loadKnownFaces(data)
    const matcher = new faceapi.FaceMatcher(knownFaces, 0.6)

    setInterval(async () => {
      const detection = await faceapi
        .detectSingleFace(video)
        .withFaceLandmarks()
        .withFaceDescriptor()

      if (detection) {
        const result = matcher.findBestMatch(detection.descriptor)

        if (result.label !== 'unknown') {
          stu_name = result.label
          const parts = stu_name.split("_");
          
          body = document.getElementById("student-list")
          var newDiv = document.createElement("div");
          newDiv.className = "student-item"; 
          body.appendChild(newDiv);

          var newname = document.createElement("span");
          newname.textContent = parts[0]
          newDiv.appendChild(newname);

          var attendance = document.createElement("span");
          attendance.className = "status-present"; 
          attendance.textContent = 'Present'
          newDiv.appendChild(attendance);
          
          fetch('/attendance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ studentId: result.label })
          })
        }
        else {
          console.log('unknown')
        }
      }
    }, 2000)
  })
})