document.addEventListener('DOMContentLoaded', function() {
    const statusFilter = document.getElementById('statusFilter');
    const searchInput = document.getElementById('searchInput');
    const tableRows = document.querySelectorAll('table tbody tr');

    statusFilter.addEventListener('change', function() {
        filterAndSearch(); // Call the filtering and searching function
    });

    searchInput.addEventListener('keyup', function() {
        filterAndSearch(); // Call the filtering and searching function
    });

    function filterAndSearch() {
        const searchText = searchInput.value.toLowerCase();
        const filterValue = statusFilter.value;

        tableRows.forEach(row => {
            const cells = row.getElementsByTagName('td');
            const status = cells[2] ? cells[2].textContent : '';
            const text = row.textContent.toLowerCase();
            const statusMatch = !filterValue || status.trim() === filterValue;
            const textMatch = !searchText || text.includes(searchText);
            if (statusMatch && textMatch) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
});