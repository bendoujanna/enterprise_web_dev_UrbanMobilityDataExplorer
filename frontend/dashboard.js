let charts = {};

document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupDarkMode();
    loadDashboard();
    setupFilters();
});
// navigation and view switching
function setupNavigation() {
    const links = document.querySelectorAll('.nav-links li');
    links.forEach(link => {
        link.addEventListener('click', () => {
            // Update Active State
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Switch Views
            const viewId = link.getAttribute('data-view');
            document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
            document.getElementById(`${viewId}-view`).style.display = 'block';

            // Load Data for Specific Views
            if (viewId === 'dashboard') loadDashboard();
            if (viewId === 'analytics') loadAnalytics();
            if (viewId === 'quality') loadQuality();
        });
    });
}
// dark mode
function setupDarkMode() {
    const toggle = document.getElementById('dark-mode-toggle');
    if (!toggle) return;

    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
        // Refresh charts to apply new theme colors
        Object.values(charts).forEach(c => c.update());
    });
}

// dashboard
async function loadDashboard() {
    // Fetch all data in parallel for speed
    const [summary, quality, boroughs, speed] = await Promise.all([
        API.getSummary(),
        API.getQuality(),
        API.getBoroughDist(),
        API.getSpeedEff()
    ]);

    // Update KPIs
    if (summary) {
        document.getElementById('total-trips').textContent = summary.total_trips.toLocaleString();
        document.getElementById('avg-fare').textContent = `$${summary.avg_fare}`;
    }
    if (quality) {
        document.getElementById('quality-score').textContent = quality.overall_score;
        document.getElementById('rejected-count-text').textContent = `${quality.rejected_records.toLocaleString()} rejected records`;
    }

    // Render Charts and table
    if (boroughs) renderBoroughChart(boroughs);
    if (speed) renderSpeedChart(speed);
    loadTripsTable(); // Initial load
}

// analytics
async function loadAnalytics() {
    const data = await API.getAnalytics();

    if (data) {
        document.getElementById('total-revenue').textContent = data.kpis.total_revenue;
        document.getElementById('avg-duration').textContent = data.kpis.avg_trip_duration;
        renderHourlyChart(data.chart_data);
    }
}