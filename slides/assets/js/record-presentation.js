// Record presentation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Create button container
    let buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = 'position: fixed; top: 10px; left: 10px; z-index: 1000; display: flex; align-items: center; gap: 5px;';
    
    // Create record button with icon
    let recordButton = document.createElement('button');
    recordButton.innerHTML = '⏺️';
    recordButton.title = 'Record Presentation';
    recordButton.style.cssText = `
        width: 30px;
        height: 30px;
        padding: 3px;
        background: transparent;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s;
    `;

    // Add hover effect
    recordButton.onmouseover = () => recordButton.style.transform = 'scale(1.1)';
    recordButton.onmouseout = () => recordButton.style.transform = 'scale(1)';

    buttonContainer.appendChild(recordButton);
    document.body.appendChild(buttonContainer);

    let isRecording = false;
    let stream = null;
    let mediaRecorder = null;

    // Function to start recording
    async function startRecording() {
        try {
            // First, show audio setup reminder
            alert('Please ensure:\n1. System audio output is set to BlackHole\n2. Browser audio input is set to BlackHole');

            // Get both screen and audio
            const displayStream = await navigator.mediaDevices.getDisplayMedia({
                video: { 
                    cursor: "always",
                    frameRate: { ideal: 30 }
                },
                audio: {
                    echoCancellation: false,
                    noiseSuppression: false,
                    autoGainControl: false
                }
            });

            // Get audio stream specifically from BlackHole
            const audioStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: false,
                    noiseSuppression: false,
                    autoGainControl: false,
                    deviceId: await getBlackHoleDeviceId()
                }
            });

            // Combine the streams
            stream = new MediaStream([
                ...displayStream.getVideoTracks(),
                ...audioStream.getAudioTracks()
            ]);

            // Create MediaRecorder
            const mime = MediaRecorder.isTypeSupported("video/webm; codecs=vp9") 
                      ? "video/webm; codecs=vp9" 
                      : "video/webm";
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: mime
            });

            // Array to store chunks of video data
            const chunks = [];
            mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

            // When recording stops, create and download the video
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: mime });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'presentation-recording.webm';
                a.click();
                URL.revokeObjectURL(url);
            };

            // Start recording
            mediaRecorder.start();
            recordButton.innerHTML = '⏹️';
            recordButton.title = 'Stop Recording';
            isRecording = true;

        } catch (err) {
            console.error("Error: " + err);
            alert('Recording failed: ' + err.message);
        }
    }

    // Function to stop recording
    function stopRecording() {
        if (mediaRecorder && stream) {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
            recordButton.innerHTML = '⏺️';
            recordButton.title = 'Record Presentation';
            isRecording = false;
        }
    }

    // Handle record button click
    recordButton.addEventListener('click', async () => {
        if (isRecording) {
            stopRecording();
        } else {
            // Get the start button
            const startButton = document.querySelector('#start-presentation');
            if (startButton) {
                // Start recording when user clicks record
                await startRecording();
                
                // Add listener for the start button
                startButton.addEventListener('click', () => {
                    // Recording is already running when presentation starts
                    console.log('Presentation started while recording');
                }, { once: true });
            } else {
                alert('Please wait for the presentation to load completely before starting the recording.');
            }
        }
    });

    // Helper function to get BlackHole device ID
    async function getBlackHoleDeviceId() {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const blackhole = devices.find(device => 
            device.kind === 'audioinput' && device.label.toLowerCase().includes('blackhole'));
        return blackhole ? blackhole.deviceId : null;
    }
});
