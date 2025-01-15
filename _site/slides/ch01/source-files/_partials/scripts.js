document.addEventListener('DOMContentLoaded', function() {
    // Handle slide transitions
    Reveal.on('slidechanged', function(event) {
        // Stop all audio elements
        document.querySelectorAll('audio').forEach(audio => {
            audio.pause();
            audio.currentTime = 0;
        });
    });

    // Initialize audio elements
    document.querySelectorAll('audio').forEach(audio => {
        audio.preload = 'none';  // Don't preload audio
        
        // Add ended event listener
        audio.addEventListener('ended', function() {
            this.currentTime = 0;  // Reset to beginning
        });
    });
});
