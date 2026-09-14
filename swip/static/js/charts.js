// SWIP Charts logic
// Exposes window.updateIrrigationChart to be called when weather data is loaded

window.updateIrrigationChart = function(weatherData) {
    const chartDiv = document.getElementById('irrigation-chart');
    if (!chartDiv || !weatherData || !weatherData.forecast || weatherData.forecast.length === 0) return;

    // Use Plotly to draw a bar chart of recommended irrigation
    // Recommended irrigation can be approximated as ET0 - Rainfall, bounded by 0
    
    const dates = [];
    const recommendedIrrigation = [];
    const rainfall = [];
    const et0 = [];

    weatherData.forecast.forEach(day => {
        const d = new Date(day.date).toLocaleDateString([], {weekday: 'short'});
        dates.push(d);
        
        const r = day.precipitation || 0;
        const e = day.et0 || 5.0;
        
        rainfall.push(r);
        et0.push(e);
        
        // Simple logic for irrigation recommendation:
        // if ET0 > Rainfall, we need to irrigate the difference
        const need = Math.max(0, e - r);
        recommendedIrrigation.push(Number(need.toFixed(1)));
    });

    const traceIrrigation = {
        x: dates,
        y: recommendedIrrigation,
        name: 'Recommended Irrigation (mm)',
        type: 'bar',
        marker: {
            color: 'rgba(67, 160, 71, 0.7)',
            line: {
                color: 'rgba(67, 160, 71, 1)',
                width: 1
            }
        }
    };

    const traceRainfall = {
        x: dates,
        y: rainfall,
        name: 'Forecast Rainfall (mm)',
        type: 'bar',
        marker: {
            color: 'rgba(49, 130, 206, 0.7)',
            line: {
                color: 'rgba(49, 130, 206, 1)',
                width: 1
            }
        }
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            color: '#FFFFFF',
            family: 'Inter, sans-serif'
        },
        margin: { t: 40, b: 40, l: 40, r: 20 },
        legend: {
            orientation: 'h',
            y: 1.1
        },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)',
            title: 'Millimeters (mm)'
        }
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot(chartDiv, [traceRainfall, traceIrrigation], layout, config);
};
