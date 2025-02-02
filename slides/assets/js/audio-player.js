// Audio player functionality for Reveal.js slides
document.addEventListener('DOMContentLoaded', function() {
    let currentAudio = null;
    let isTransitioning = false;
    let presentationStarted = false;

    // Function to stop current audio
    function stopCurrentAudio() {
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
        }
    }

    // Function to handle slide transitions
    function handleSlideTransition(event) {
        if (!presentationStarted || isTransitioning) return;
        isTransitioning = true;
        
        console.log('Slide transition detected');
        
        // Stop any currently playing audio
        stopCurrentAudio();
        
        const currentSlide = event.currentSlide;
        const indices = Reveal.getIndices();
        
        // Special handling for title slide
        if (indices.h === 0) {
            const audioSource = currentSlide.querySelector('.audio-source audio');
            if (audioSource) {
                currentAudio = audioSource;
                setTimeout(() => {
                    const playPromise = currentAudio.play();
                    if (playPromise !== undefined) {
                        playPromise.catch(error => {
                            console.log("Title slide audio error:", error);
                            // If audio fails, advance after 3 seconds
                            setTimeout(() => {
                                Reveal.next();
                            }, 3000);
                        });
                    }
                }, 300);

                // When title audio ends, advance after 1 second
                currentAudio.addEventListener('ended', () => {
                    setTimeout(() => {
                        Reveal.next();
                    }, 1000);
                });
            } else {
                // No audio on title slide, advance after 3 seconds
                setTimeout(() => {
                    Reveal.next();
                }, 3000);
            }
            isTransitioning = false;
            return;
        }

        // Handle all other slides
        setTimeout(() => {
            const audioSource = currentSlide.querySelector('.audio-source audio');
            
            if (audioSource) {
                currentAudio = audioSource;
                
                // Add a small delay before playing
                setTimeout(() => {
                    const playPromise = currentAudio.play();
                    if (playPromise !== undefined) {
                        playPromise.catch(error => {
                            console.log("Audio playback error:", error);
                            Reveal.configure({ autoSlide: 5000 });
                        });
                    }
                }, 300);

                // Prevent auto-advance until audio finishes
                Reveal.configure({ autoSlide: 0 });

                currentAudio.addEventListener('ended', () => {
                    // Wait a moment after audio ends before enabling auto-advance
                    setTimeout(() => {
                        Reveal.configure({ autoSlide: 5000 });
                    }, 1000);
                });
            } else {
                // If no audio, set normal auto-advance timing
                Reveal.configure({ autoSlide: 5000 });
            }
        }, 100);
        
        isTransitioning = false;
    }

    // Configure Reveal.js
    Reveal.configure({
        autoSlide: 0,
        loop: false,
        autoPlayMedia: false,
        keyboard: false // Disable keyboard navigation initially
    });

    // Initialize audio player
    window.addEventListener('load', () => {
        // Prevent any transitions until start button is clicked
        Reveal.configure({ touch: false }); // Disable touch navigation
        
        // Set up Reveal.js event listeners
        Reveal.on('slidechanged', handleSlideTransition);
    });

    // Start presentation and handle first slide
    const startButton = document.querySelector('#start-presentation');
    const startOverlay = document.querySelector('#start-overlay');
    
    if (startButton && startOverlay) {
        startButton.addEventListener('click', () => {
            presentationStarted = true;
            startOverlay.style.display = 'none';
            
            // Re-enable navigation after start
            Reveal.configure({ 
                keyboard: true,
                touch: true
            });
            
            // Start from the first slide
            Reveal.slide(0);
            handleSlideTransition({ currentSlide: Reveal.getCurrentSlide() });
        });
    }

    // Handle manual navigation
    Reveal.on('fragmentshown', () => {
        if (!presentationStarted) return;
        stopCurrentAudio();
    });
    Reveal.on('fragmenthidden', () => {
        if (!presentationStarted) return;
        stopCurrentAudio();
    });
});
