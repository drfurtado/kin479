const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const multer = require('multer');
const upload = multer();

const app = express();
app.use(cors());

// Proxy endpoint for Together.ai API
app.post('/api/together-proxy', upload.none(), async (req, res) => {
    try {
        const { request, apiKey } = req.body;
        
        if (!request || !apiKey) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }

        const requestData = JSON.parse(request);
        
        const response = await fetch('https://api.together.xyz/v2/images/generations', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const error = await response.text();
            console.error('Together.ai API error:', error);
            return res.status(response.status).send(error);
        }

        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('Proxy error:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Proxy server running on port ${PORT}`);
});
