document.addEventListener('DOMContentLoaded', function() {
    // Load and plot historical and predicted data
    d3.csv('data/predictions.csv').then(function(data) {
        const ctx = document.getElementById('chart').getContext('2d');
        
        const dates = data.map(row => row['Date']);
        const closePrices = data.map(row => parseFloat(row['Close']));
        const predictedPrices = data.map(row => parseFloat(row['Predictions']));
        
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
                        borderColor: 'crimson',
                        backgroundColor: 'rgba(255, 100, 100, 0.5)',
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
                            text: 'Date',
                            color: '#e0e0e0',
                            font: {
                                size: 14,
                                family: 'Orkney'
                            }
                        },
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 20,
                            maxRotation: 45,
                            minRotation: 45,
                            color: '#e0e0e0',
                            font: {
                                size: 12,
                                family: 'Orkney'
                            }
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Price',
                            color: '#e0e0e0',
                            font: {
                                size: 14,
                                family: 'Orkney'
                            }
                        },
                        ticks: {
                            color: '#e0e0e0',
                            font: {
                                size: 12,
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
    });

    // Load and display next day prediction
    d3.csv('data/future_predictions.csv').then(function(data) {
        const nextDayPrediction = data[0];
        const suggestionText = `Date: ${nextDayPrediction['']},
        Predicted Close: ${nextDayPrediction['Predicted_Close']},
        Signal: ${nextDayPrediction['Signal']}`;
        
        document.getElementById('suggestion').textContent = suggestionText;
    });
});
