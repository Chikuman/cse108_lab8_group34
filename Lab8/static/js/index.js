function showTab(tab) {
    document.getElementById('current-classes').style.display =
        tab === 'current' ? 'block' : 'none';

    document.getElementById('add-classes').style.display =
        tab === 'add' ? 'block' : 'none';
}