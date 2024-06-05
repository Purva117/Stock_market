document.addEventListener('DOMContentLoaded', () => {
    const apiKey = 'YOUR_API_KEY'; // Placeholder that will be replaced

    const symbol = 'AAPL'; // Example stock symbol

    async function fetchStockData() {
        try {
            const response = await fetch(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&apikey=${apiKey}`);
            const data = await response.json();
            displayStockData(data);
            displayMetrics(data);
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    }

    function displayStockData(data) {
        const timeSeries = data['Time Series (Daily)'];
        const dates = Object.keys(timeSeries).sort((a, b) => new Date(b) - new Date(a));
        const latestDate = dates[0];
        const latestData = timeSeries[latestDate];
        
        const priceContainer = document.getElementById('price-container');
        priceContainer.innerHTML = `
            <p>Date: ${latestDate}</p>
            <p>Open: $${latestData['1. open']}</p>
            <p>High: $${latestData['2. high']}</p>
            <p>Low: $${latestData['3. low']}</p>
            <p>Close: $${latestData['4. close']}</p>
        `;
    }

    function displayMetrics(data) {
        const timeSeries = data['Time Series (Daily)'];
        const dates = Object.keys(timeSeries).sort((a, b) => new Date(b) - new Date(a));
        const latestDate = dates[0];
        const latestData = timeSeries[latestDate];
        
        // Simple Moving Average for the last 10 days
        const closePrices = dates.slice(0, 10).map(date => parseFloat(timeSeries[date]['4. close']));
        const sma10 = closePrices.reduce((acc, price) => acc + price, 0) / closePrices.length;

        const metricsContainer = document.getElementById('metrics-container');
        metricsContainer.innerHTML = `
            <p>10-Day Simple Moving Average (SMA): $${sma10.toFixed(2)}</p>
            <p>Recommendation: ${latestData['4. close'] > sma10 ? 'Buy' : 'Sell'}</p>
        `;
    }

    fetchStockData();
});
