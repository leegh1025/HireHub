document.addEventListener('DOMContentLoaded', function () {
    const query = new URLSearchParams(window.location.search);
    const sortOrder = query.get('sort');
    if (sortOrder) {
        document.getElementById('sortOrder').value = sortOrder;
    }
});

document.getElementById('sortOrder').addEventListener('change', function () {
    const selectedValue = this.value;
    const query = new URLSearchParams(window.location.search);
    query.set('sort', selectedValue);
    window.location.search = query.toString();
});