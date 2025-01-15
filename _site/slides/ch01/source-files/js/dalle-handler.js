document.addEventListener('DOMContentLoaded', async function() {
    console.log('DALL-E handler initialized');
    
    // Wait for Reveal to be ready
    if (typeof Reveal !== 'undefined') {
        Reveal.addEventListener('ready', async function() {
            console.log('Reveal is ready, initializing DALL-E');
            await initDallE();
        });
    } else {
        console.error('Reveal.js not found');
    }
});

async function initDallE() {
    try {
        console.log('Loading DALL-E config...');
        const { generateDalleImage } = await import('./dalle-config.js');
        const containers = document.querySelectorAll('.dalle-container');
        console.log('Found DALL-E containers:', containers.length);

        containers.forEach(async (container) => {
            const prompt = container.dataset.prompt;
            if (prompt) {
                console.log('Processing prompt:', prompt);
                try {
                    const loadingText = document.createElement('div');
                    loadingText.textContent = 'Generating image...';
                    container.appendChild(loadingText);

                    const imageUrl = await generateDalleImage(prompt);
                    loadingText.remove();

                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.className = 'dalle-generated-image';
                    container.appendChild(img);
                } catch (error) {
                    console.error('Error generating image:', error);
                    const errorText = document.createElement('div');
                    errorText.textContent = 'Failed to generate image: ' + error.message;
                    errorText.style.color = 'red';
                    container.appendChild(errorText);
                }
            }
        });
    } catch (error) {
        console.error('Failed to initialize DALL-E:', error);
    }
}
