document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    let currentAudio = null;
    let isTransitioning = false;
    let presentationStarted = false;
    let currentEndedHandler = null;

    // Function to stop current audio and clean up event listeners
    function stopCurrentAudio() {
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            if (currentEndedHandler) {
                currentAudio.removeEventListener('ended', currentEndedHandler);
                currentEndedHandler = null;
            }
        }
    }

    // Handle slide transitions
    function handleSlideChange(event) {
        console.log('Slide change triggered', { presentationStarted, isTransitioning });
        if (!presentationStarted || isTransitioning) return;
        isTransitioning = true;
        
        // Stop any currently playing audio and clean up
        stopCurrentAudio();
        
        const currentSlide = event.currentSlide || Reveal.getCurrentSlide();
        console.log('Current slide:', currentSlide);
        const audioSource = currentSlide.querySelector('.audio-source audio');
        
        if (audioSource) {
            // Disable auto-advance while audio is playing
            Reveal.configure({ autoSlide: 0 });
            currentAudio = audioSource;
            
            // Create new ended handler
            currentEndedHandler = () => {
                setTimeout(() => {
                    if (currentAudio === audioSource) { // Only advance if this is still the current audio
                        Reveal.next();
                    }
                }, 1000);
            };
            
            // Add new ended handler
            currentAudio.addEventListener('ended', currentEndedHandler);
            
            // Play audio after a short delay
            setTimeout(() => {
                if (currentAudio === audioSource) { // Only play if this is still the current audio
                    const playPromise = currentAudio.play();
                    if (playPromise !== undefined) {
                        playPromise.catch(error => {
                            console.log("Audio playback error:", error);
                            Reveal.configure({ autoSlide: 5000 });
                        });
                    }
                }
            }, 300);
        } else {
            // No audio on this slide, set 5-second auto-advance
            Reveal.configure({ autoSlide: 5000 });
        }
        
        isTransitioning = false;
    }

    // Initialize presentation controls
    const startButton = document.getElementById('start-presentation');
    const startOverlay = document.getElementById('start-overlay');
    
    console.log('Start elements:', { startButton, startOverlay });
    
    if (startButton && startOverlay) {
        console.log('Adding click listener to start button');
        startButton.addEventListener('click', function() {
            console.log('Start button clicked');
            startOverlay.style.display = 'none';
            presentationStarted = true;
            
            // Configure Reveal
            console.log('Configuring Reveal.js');
            Reveal.configure({ 
                keyboard: true,
                touch: true,
                autoSlide: 0
            });
            
            // Set up slide change listener
            console.log('Setting up slide change listener');
            Reveal.on('slidechanged', handleSlideChange);
            
            // Force a layout update
            console.log('Forcing layout update');
            window.dispatchEvent(new Event('resize'));
            
            // Start from beginning and handle first slide
            console.log('Starting presentation');
            Reveal.slide(0);
            handleSlideChange({ currentSlide: Reveal.getCurrentSlide() });
        });
    } else {
        console.error('Start button or overlay not found!');
    }

    // Handle manual navigation
    Reveal.on('fragmentshown', stopCurrentAudio);
    Reveal.on('fragmenthidden', stopCurrentAudio);
});
