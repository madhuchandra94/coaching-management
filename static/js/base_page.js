function openPanel(id) {
    const panel = document.getElementById(id);
    const isActive = panel.classList.contains('active');

    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

    if (!isActive) {
        panel.classList.add('active');
    }
}