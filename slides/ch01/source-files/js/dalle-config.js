// Import local configuration
import { CONFIG } from './config.local.js';

// DALL-E API Configuration
const DALLE_CONFIG = {
    apiKey: CONFIG.OPENAI_API_KEY,
    model: 'dall-e-3', // Using DALL-E 3 for higher quality images
    size: '1024x1024', // Standard size
    quality: 'standard',
    n: 1 // Number of images to generate
};

// Function to generate images using DALL-E
async function generateDalleImage(prompt) {
    try {
        console.log('Making API request to DALL-E with config:', {
            model: DALLE_CONFIG.model,
            size: DALLE_CONFIG.size,
            quality: DALLE_CONFIG.quality,
            apiKeyLength: DALLE_CONFIG.apiKey?.length || 0
        });

        const response = await fetch('https://api.openai.com/v1/images/generations', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${DALLE_CONFIG.apiKey}`,
                'OpenAI-Organization': CONFIG.OPENAI_ORG_ID // Optional: add if you have an org ID
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

// Export the function for use in other files
export { generateDalleImage };
