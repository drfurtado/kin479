// DALL-E API Configuration
const DALLE_CONFIG = {
    apiKey: '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',
    model: 'dall-e-3',
    size: '1024x1024',
    quality: 'standard',
    n: 1
};

// Function to generate images using DALL-E
async function generateDalleImage(prompt) {
    try {
        console.log('Making API request to DALL-E...');
        const response = await fetch('https://api.openai.com/v1/images/generations', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${DALLE_CONFIG.apiKey}`
            },
            body: JSON.stringify({
                model: DALLE_CONFIG.model,
                prompt: prompt,
                n: DALLE_CONFIG.n,
                size: DALLE_CONFIG.size,
                quality: DALLE_CONFIG.quality
            })
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('API Error Response:', errorData);
            throw new Error(`HTTP error! status: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('API Response:', data);
        
        if (!data.data?.[0]?.url) {
            throw new Error('No image URL in response');
        }
        
        return data.data[0].url;
    } catch (error) {
        console.error('Error in generateDalleImage:', error);
        throw error;
    }
}

// Initialize DALL-E when the document is ready
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
        const containers = document.querySelectorAll('.dalle-container');
        console.log('Found DALL-E containers:', containers.length);

        containers.forEach(async (container) => {
            const prompt = container.dataset.prompt;
            if (prompt) {
                console.log('Processing prompt:', prompt);
                try {
                    const loadingText = document.createElement('div');
                    loadingText.textContent = 'Generating AI image...';
                    loadingText.className = 'loading-text';
                    container.appendChild(loadingText);

                    const imageUrl = await generateDalleImage(prompt);
                    loadingText.remove();

                    const imgWrapper = document.createElement('div');
                    imgWrapper.style.width = '100%';
                    
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.className = 'dalle-generated-image';
                    img.alt = 'AI-generated illustration';
                    
                    imgWrapper.appendChild(img);
                    container.appendChild(imgWrapper);
                } catch (error) {
                    console.error('Error generating image:', error);
                    const errorText = document.createElement('div');
                    errorText.textContent = 'Failed to generate image: ' + error.message;
                    errorText.className = 'error-text';
                    container.appendChild(errorText);
                }
            }
        });
    } catch (error) {
        console.error('Failed to initialize DALL-E:', error);
    }
}
