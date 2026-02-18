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