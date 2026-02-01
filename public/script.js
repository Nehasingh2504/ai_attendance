const video = document.getElementById('video')

Promise.all([
  faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/models')
]).then(startVideo)

function startVideo() {
  navigator.mediaDevices.getUserMedia({ video: {} })
    .then(stream => video.srcObject = stream)
}

async function loadKnownFaces() {
  const labels = ['Max_1','neha_1']
  
  return Promise.all(
    labels.map(async label => {
      const img = await faceapi.fetchImage(`/known faces/class_1/${label}.jpg`)
      const detection = await faceapi
        .detectSingleFace(img)
        .withFaceLandmarks()
        .withFaceDescriptor()
      return new faceapi.LabeledFaceDescriptors(label, [detection.descriptor])
    })
  )
}

video.addEventListener('play', async () => {
  const knownFaces = await loadKnownFaces()
  const matcher = new faceapi.FaceMatcher(knownFaces, 0.6)

  setInterval(async () => {
    const detection = await faceapi
      .detectSingleFace(video)
      .withFaceLandmarks()
      .withFaceDescriptor()

    if (detection) {
      const result = matcher.findBestMatch(detection.descriptor)

      if (result.label !== 'unknown') {
        console.log(result.label)
        fetch('/attendance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ studentId: result.label })
        })
      }
      else{
        console.log('unknown')
      }
    }
  }, 2000)
})
