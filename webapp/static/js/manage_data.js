document.addEventListener('DOMContentLoaded', function () {
    // Get table elements
    const table = document.getElementById('manage-data-table');
    const rows = table.getElementsByTagName('tr');

    // Entries per page
    const entriesPerPage = document.querySelector('.entries');
    let rowsPerPage = parseInt(entriesPerPage.value);

    // Function to display rows based on selected entries per page
    entriesPerPage.addEventListener('change', function () {
        rowsPerPage = parseInt(this.value);
        showRows(rowsPerPage);
    });

    // Search bar functionality
    const searchInput = document.querySelector('.search');
    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        if (query === '') {
            showRows(rowsPerPage); // If search query is empty, display rows according to current entries per page
        } else {
            filterTable(query); // If there's a search query, filter the table based on the query
        }
    });

    // Page navigation buttons
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    let currentPage = 0;

    // Display initial rows based on default entries per page
    showRows(rowsPerPage);

    // Function to display rows based on the selected entries per page
    function showRows(rowsPerPage) {
        let start = currentPage * rowsPerPage + 1;
        let end = (currentPage + 1) * rowsPerPage + 1;

        for (let i = 1; i < rows.length; i++) {
            if (i < start || i >= end) {
                rows[i].style.display = 'none';
            } else {
                rows[i].style.display = '';
            }
        }

        // Disable previous button if on the first page, disable next button if on the last page
        prevBtn.disabled = currentPage === 0;
        nextBtn.disabled = end >= rows.length;
    }

    // Function to filter table rows based on the search query
    function filterTable(query) {
        for (let i = 1; i < rows.length; i++) {
            let shouldDisplay = false;
            for (let j = 0; j < rows[i].getElementsByTagName('td').length; j++) {
                const cell = rows[i].getElementsByTagName('td')[j];
                if (cell && cell.innerHTML.toLowerCase().indexOf(query) > -1) {
                    shouldDisplay = true;
                    break;
                }
            }
            rows[i].style.display = shouldDisplay ? '' : 'none';
        }
    }

    // Functionality for previous and next page buttons
    prevBtn.addEventListener('click', function () {
        if (currentPage > 0) {
            currentPage--;
            showRows(rowsPerPage);
        }
    });

    nextBtn.addEventListener('click', function () {
        if ((currentPage + 1) * rowsPerPage < rows.length) {
            currentPage++;
            showRows(rowsPerPage);
        }
    });
});
