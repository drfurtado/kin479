// Image Generation using Stability AI API
// Requires flux-config.js to be loaded first

// Helper function to delay execution
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to enhance prompts for kinesiology-specific content
function enhancePrompt(prompt) {
    // Keep the original prompt but add style guidance
    const stylePrefix = 'Draw this as a minimal sketch focusing on human movement and anatomy: ';
    
    // Core style requirements
    const styleDirectives = [
        'use single continuous lines',
        'pencil sketch style',
        'absolute minimum detail',
        'essential lines only',
        'black lines on white',
        'transparent background',
        'focus on human form',
        'anatomical accuracy'
    ].join(', ');
    
    // Negative prompts for both style and content
    const negativePrompt = [
        'no shading',
        'no color',
        'no texture',
        'no fill',
        'no text',
        'no background',
        'no unnecessary lines',
        'no cars',
        'no vehicles',
        'no machines',
        'no robots',
        'no abstract shapes',
        'no unrelated objects'
    ].join(', ');
    
    // Human-focused content guidance
    const contentFocus = [
        'emphasize human anatomy',
        'show natural movement',
        'include skeletal structure',
        'focus on body mechanics',
        'highlight muscle groups'
    ].join(', ');
    
    // Preserve the original prompt but ensure minimal style and human focus
    return `${stylePrefix}"${prompt}". Style: ${styleDirectives}. Content focus: ${contentFocus}. Avoid: ${negativePrompt}. Make it an ultra-minimal line drawing that clearly represents human movement and anatomy.`;
}

// Function to generate images using Stability AI with retry logic
async function generateFluxImage(prompt, retryCount = 0, maxRetries = 3) {
    try {
        if (!FLUX_CONFIG || !FLUX_CONFIG.apiKey) {
            throw new Error('Flux configuration or API key not found. Please ensure flux-config.js is properly set up.');
        }

        // Enhance the prompt
        const enhancedPrompt = enhancePrompt(prompt);
        console.log('Original prompt:', prompt);
        console.log('Enhanced prompt:', enhancedPrompt);

        if (retryCount > 0) {
            console.log(`Retry attempt ${retryCount} of ${maxRetries}...`);
            await delay(Math.min(1000 * Math.pow(2, retryCount), 10000));
        }

        // Try to list available engines first
        const enginesResponse = await fetch('https://api.stability.ai/v1/engines/list', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${FLUX_CONFIG.apiKey}`
            }
        });

        if (!enginesResponse.ok) {
            console.error('Failed to list engines:', await enginesResponse.text());
            throw new Error('Failed to list available engines');
        }

        const engines = await enginesResponse.json();
        console.log('Available engines:', engines);

        // Use the first available engine
        const engineId = engines[0]?.id;
        if (!engineId) {
            throw new Error('No available engines found');
        }

        console.log('Using engine:', engineId);

        const response = await fetch(`https://api.stability.ai/v1/generation/${engineId}/text-to-image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${FLUX_CONFIG.apiKey}`
            },
            body: JSON.stringify({
                text_prompts: [
                    {
                        text: enhancedPrompt,
                        weight: 1
                    },
                    {
                        text: "inappropriate content, nudity, suggestive poses, unsafe content, graphic content",
                        weight: -1
                    },
                    {
                        text: "background, shading, fill, texture, color, gradient, solid background, white background",
                        weight: -1
                    }
                ],
                cfg_scale: FLUX_CONFIG.cfg_scale,
                height: FLUX_CONFIG.height,
                width: FLUX_CONFIG.width,
                steps: FLUX_CONFIG.steps,
                style_preset: "line-art",
                sampler: "DDIM",
                safety_filter: true
            })
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            try {
                const errorData = JSON.parse(errorText);
                throw new Error(`HTTP error! status: ${response.status} - ${errorData.message || 'Unknown error'}`);
            } catch (e) {
                throw new Error(`HTTP error! status: ${response.status} - ${errorText || 'Unknown error'}`);
            }
        }

        const data = await response.json();
        console.log('API Response structure:', JSON.stringify(data, null, 2));

        if (!data.artifacts || !data.artifacts[0] || !data.artifacts[0].base64) {
            console.error('Invalid response structure:', data);
            throw new Error('Invalid response structure from API');
        }

        // Convert to data URL
        const imageUrl = `data:image/png;base64,${data.artifacts[0].base64}`;
        console.log('Generated image URL (first 100 chars):', imageUrl.substring(0, 100) + '...');
        return imageUrl;

    } catch (error) {
        console.error('Full error:', error);
        console.error('Error stack:', error.stack);
        if (error.message.includes('429') && retryCount < maxRetries) {
            console.log('Rate limit error caught, retrying...');
            return generateFluxImage(prompt, retryCount + 1, maxRetries);
        }
        throw error;
    }
}

// Add regenerate button to each flux container
function addRegenerateButton(container) {
    const button = document.createElement('button');
    button.innerHTML = '🔄';
    button.style.position = 'relative';
    button.style.display = 'block';
    button.style.margin = '5px auto';
    button.style.width = '24px';
    button.style.height = '24px';
    button.style.padding = '0';
    button.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
    button.style.border = '1px solid #ccc';
    button.style.borderRadius = '50%';
    button.style.cursor = 'pointer';
    button.style.fontSize = '12px';
    button.style.lineHeight = '24px';
    button.style.opacity = '0.6';
    button.style.transition = 'opacity 0.3s ease';

    // Show button on container hover
    container.addEventListener('mouseenter', () => button.style.opacity = '1');
    container.addEventListener('mouseleave', () => button.style.opacity = '0.6');

    // Handle regeneration
    button.addEventListener('click', async (e) => {
        e.preventDefault();
        const promptElement = container.querySelector('.flux-prompt');
        if (!promptElement) return;

        const prompt = promptElement.textContent;
        const img = container.querySelector('img');
        if (!img) return;

        button.disabled = true;
        button.innerHTML = '⌛';
        
        try {
            const imageUrl = await generateFluxImage(prompt);
            img.src = imageUrl;
        } catch (error) {
            console.error('Failed to regenerate image:', error);
            alert('Failed to regenerate image. Please try again.');
        } finally {
            button.disabled = false;
            button.innerHTML = '🔄';
        }
    });

    container.appendChild(button);
}

// Initialize Flux functionality
window.addEventListener('load', function() {
    console.log('Flux handler initialized');
    
    // Process each flux container
    document.querySelectorAll('.flux-container').forEach(async (container) => {
        const prompt = container.getAttribute('data-prompt');
        if (!prompt) {
            console.error('No prompt found for container:', container);
            return;
        }
        
        // Create hidden prompt element
        const promptElement = document.createElement('div');
        promptElement.className = 'flux-prompt';
        promptElement.style.display = 'none';
        promptElement.textContent = prompt;
        container.appendChild(promptElement);
        
        // Create image element
        const img = document.createElement('img');
        img.className = 'flux-generated-image';
        container.appendChild(img);
        
        // Add regenerate button
        addRegenerateButton(container);
        
        try {
            const imageUrl = await generateFluxImage(prompt);
            img.src = imageUrl;
        } catch (error) {
            console.error('Failed to generate image:', error);
            img.alt = 'Failed to generate image';
            img.style.display = 'none';
        }
    });
});
