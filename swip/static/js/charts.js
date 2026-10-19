// Accessible bars and table use the authoritative forecast water-balance response only.
window.updateIrrigationChart = function(plan) {
    const container = document.getElementById('irrigation-chart');
    if (!container) return;
    container.replaceChildren();
    if (plan?.status !== 'available' || !plan.days?.length) {
        container.textContent = 'No validated seven-day scenario available. Run analysis with an available forecast; no values are generated offline.';
        return;
    }
    const table = document.createElement('table');
    table.className = 'data-table';
    const caption = document.createElement('caption');
    caption.textContent = 'Forecast water-balance scenario, not scheduled irrigation. Dates: Asia/Dushanbe.';
    table.appendChild(caption);
    const head = table.createTHead().insertRow();
    ['Date', 'Forecast rain (mm)', 'Net deficit (mm)', 'Gross water (L)'].forEach(label => {
        const cell = document.createElement('th');
        cell.scope = 'col';
        cell.textContent = label;
        head.appendChild(cell);
    });
    const body = table.createTBody();
    const maximum = Math.max(1, ...plan.days.map(day => day.amount_mm));
    for (const day of plan.days) {
        const row = body.insertRow();
        for (const value of [day.date, day.rainfall_mm, day.amount_mm, day.water_liters]) {
            row.insertCell().textContent = value;
        }
        const bar = document.createElement('div');
        bar.className = 'plan-bar';
        bar.style.width = Math.max(0, day.amount_mm / maximum * 100) + '%';
        bar.setAttribute('aria-hidden', 'true');
        row.cells[2].appendChild(bar);
    }
    container.appendChild(table);
};
