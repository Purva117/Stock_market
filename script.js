document.addEventListener('DOMContentLoaded', function() {
    // Load and plot historical and predicted data
    d3.csv('data/predictions.csv').then(function(data) {
        const ctx = document.getElementById('chart').getContext('2d');

        const dates = data.map(row => row['Date']);
        const closePrices = data.map(row => parseFloat(row['Close']));
        const predictedPrices = data.map(row => parseFloat(row['Predictions']));

        // Load and display additional stats
        d3.csv('data/model_performance.csv').then(function(performanceData) {
            const performance = performanceData[0];
            const mse = parseFloat(performance['MSE']).toFixed(2);
            const mae = parseFloat(performance['MAE']).toFixed(2);
            const r2 = parseFloat(performance['R2']).toFixed(2);

            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [
                        {
                            label: 'Actual Close Prices',
                            data: closePrices,
                            borderColor: 'skyblue',
                            backgroundColor: 'rgba(135, 206, 235, 0.5)',
                            fill: false
                        },
                        {
                            label: 'Predicted Prices',
                            data: predictedPrices,
                            borderColor: 'yellow',
                            backgroundColor: 'rgba(255, 255, 0, 0.5)',
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                color: '#e0e0e0',
                                font: {
                                    size: 22,
                                    family: 'Orkney',
                                }
                            },
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 12,
                                maxRotation: 90,
                                minRotation: 0,
                                color: '#e0e0e0',
                                font: {
                                    size: 16,
                                    family: 'Orkney',
                                },
                                callback: function(value, index, values) {
                                    const date = new Date(dates[index]);
                                    const options = { year: 'numeric', month: 'short'};
                                    return date.toLocaleDateString('en-US', options);
                                }
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Price (USD)',
                                color: '#e0e0e0',
                                font: {
                                    size: 20,
                                    family: 'Orkney'
                                }
                            },
                            ticks: {
                                color: '#e0e0e0',
                                font: {
                                    size: 16,
                                    family: 'Orkney'
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom',
                            align: 'end',
                            labels: {
                                color: '#e0e0e0',
                                font: {
                                    size: 15,
                                    family: 'Orkney'
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: '#333',
                            titleColor: '#e0e0e0',
                            bodyColor: '#e0e0e0',
                            borderColor: '#444',
                            borderWidth: 1
                        }
                    },
                    layout: {
                        padding: {
                            left: 0,
                            right: 0,
                            top: 0,
                            bottom: 0
                        }
                    }
                }
            });

            // Apply dark background to the chart area
            ctx.canvas.parentNode.style.backgroundColor = '#1e1e1e';

            // Add stats box
            const statsBox = document.createElement('div');
            statsBox.id = 'stats-box';
            statsBox.innerHTML = `
                <h4>Model Performance Stats</h4>
                <p>Mean Sq. Error: ${mse}</p>
                <p>Mean Abs. Error: ${mae}</p>
                <p>R²: ${r2}</p>
            `;
            ctx.canvas.parentNode.appendChild(statsBox);
        });
    });

    // Load and display next day prediction
    d3.csv('data/future_predictions.csv').then(function(data) {
        const nextDayPrediction = data[0];
        const formattedClose = parseFloat(nextDayPrediction['Predicted_Close']).toFixed(2);
        const suggestionText = `
            <p>Date: ${nextDayPrediction['']}</p>
            <p>Predicted Close: ${formattedClose}</p>
            <p>Signal: <span style="color: ${nextDayPrediction['Signal'] === 'BUY' ? 'green' : 'red'};">${nextDayPrediction['Signal']}</span></p>
        `;
        document.getElementById('suggestion').innerHTML = suggestionText;
    });
});
