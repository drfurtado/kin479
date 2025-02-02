document.addEventListener('DOMContentLoaded', function() {
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
        if (!presentationStarted || isTransitioning) return;
        isTransitioning = true;
        
        // Stop any currently playing audio and clean up
        stopCurrentAudio();
        
        const currentSlide = event.currentSlide || Reveal.getCurrentSlide();
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
    
    if (startButton && startOverlay) {
        startButton.addEventListener('click', function() {
            startOverlay.style.display = 'none';
            presentationStarted = true;
            
            // Configure Reveal
            Reveal.configure({ 
                keyboard: true,
                touch: true,
                autoSlide: 0
            });
            
            // Set up slide change listener
            Reveal.on('slidechanged', handleSlideChange);
            
            // Force a layout update
            window.dispatchEvent(new Event('resize'));
            
            // Start from beginning and handle first slide
            Reveal.slide(0);
            handleSlideChange({ currentSlide: Reveal.getCurrentSlide() });
        });
    }

    // Handle manual navigation
    Reveal.on('fragmentshown', stopCurrentAudio);
    Reveal.on('fragmenthidden', stopCurrentAudio);
});
