// Plotly charts implementation
async function loadAnalytics() {
    const res = await fetch('/api/history');
    const data = await res.json();
    const history = data.history.reverse(); // oldest to newest for trend
    
    if(history.length === 0) return;

    const dates = history.map(h => new Date(h.timestamp).toLocaleDateString());
    const lang = document.getElementById('lang-select').value;
    
    // 1. Risk Trend (Blue Accent)
    const riskScores = history.map(h => h.risk_score);
    const trace1 = {
        x: dates,
        y: riskScores,
        type: 'scatter',
        mode: 'lines+markers',
        line: {color: '#1976D2', width: 3, shape: 'spline'},
        marker: {size: 8, color: '#1976D2', symbol: 'circle', line: {color: '#ffffff', width: 1.5}},
        name: 'Risk Score'
    };
    const layout1 = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: {family: 'Inter, sans-serif', color: '#94a3b8', size: 11},
        margin: {t: 20, l: 40, r: 20, b: 40},
        xaxis: {
            gridcolor: 'rgba(255, 255, 255, 0.05)',
            zeroline: false,
            tickfont: {color: '#94a3b8'}
        },
        yaxis: {
            gridcolor: 'rgba(255, 255, 255, 0.05)',
            zeroline: false,
            range: [0, 105],
            tickfont: {color: '#94a3b8'}
        }
    };
    Plotly.newPlot('chart-risk', [trace1], layout1, {displayModeBar: false, responsive: true});

    // 2. Crop Distribution (Agricultural Greens & Blues)
    const cropCounts = {};
    history.forEach(h => {
        const cropKey = 'crop_' + h.crop_type.toLowerCase();
        const translatedCrop = (translations[lang] && translations[lang][cropKey]) ? translations[lang][cropKey] : h.crop_type;
        cropCounts[translatedCrop] = (cropCounts[translatedCrop] || 0) + 1;
    });
    const trace2 = {
        labels: Object.keys(cropCounts),
        values: Object.values(cropCounts),
        type: 'pie',
        hole: 0.55,
        marker: {
            colors: ['#1B5E20', '#43A047', '#1976D2', '#81c784', '#64b5f6', '#ffd54f'],
            line: {color: '#1E293B', width: 2}
        },
        textinfo: 'percent',
        textposition: 'inside',
        insidetextorientation: 'radial'
    };
    const layout2 = {
        paper_bgcolor: 'transparent',
        font: {family: 'Inter, sans-serif', color: '#94a3b8', size: 11},
        margin: {t: 20, l: 20, r: 20, b: 20},
        showlegend: true,
        legend: {
            font: {color: '#94a3b8'},
            orientation: 'h',
            yanchor: 'bottom',
            y: -0.25,
            xanchor: 'center',
            x: 0.5
        }
    };
    Plotly.newPlot('chart-crops', [trace2], layout2, {displayModeBar: false, responsive: true});

    // 3. Water Usage Trend (Emerald Green Bars)
    const waterReq = history.map(h => h.water_required);
    const trace3 = {
        x: dates,
        y: waterReq,
        type: 'bar',
        marker: {
            color: 'rgba(67, 160, 71, 0.4)',
            line: {color: '#43A047', width: 2}
        }
    };
    const layout3 = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: {family: 'Inter, sans-serif', color: '#94a3b8', size: 11},
        margin: {t: 20, l: 60, r: 20, b: 40},
        xaxis: {
            gridcolor: 'rgba(255, 255, 255, 0.05)',
            zeroline: false,
            tickfont: {color: '#94a3b8'}
        },
        yaxis: {
            gridcolor: 'rgba(255, 255, 255, 0.05)',
            zeroline: false,
            title: translations[lang].lbl_liters,
            titlefont: {color: '#94a3b8'},
            tickfont: {color: '#94a3b8'}
        }
    };
    Plotly.newPlot('chart-water', [trace3], layout3, {displayModeBar: false, responsive: true});
}
