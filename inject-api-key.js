const fs = require('fs');

const apiKey = process.env.ALPHA_VANTAGE_API_KEY;

fs.readFile('script.js', 'utf8', (err, data) => {
    if (err) throw err;
    const result = data.replace('YOUR_API_KEY', apiKey);

    fs.writeFile('script.js', result, 'utf8', (err) => {
        if (err) throw err;
        console.log('API key injected successfully!');
    });
});
