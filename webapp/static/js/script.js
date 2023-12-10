document.addEventListener('DOMContentLoaded', function() {
    // Functionality for removing messages
    const removeButtons = document.querySelectorAll('.remove-message');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentNode.remove(); // Remove the entire <li> when the button is clicked
        });
    });

    // Function to handle table selection and submission
    const handleTableSelection = (formId) => {
        document.getElementById(formId).submit();
    };

    // Handling fileForm and tableForm change events for table selection

    const tableForm = document.getElementById('tableForm');
    if (tableForm) {
        tableForm.addEventListener('change', function() {
            handleTableSelection('tableForm');
        });
    }

    // Function to show table rows based on pagination
    const showPage = (tableRows, currentPage, rowsPerPage) => {
        const startIndex = (currentPage - 1) * rowsPerPage;
        const endIndex = currentPage * rowsPerPage;

        tableRows.forEach((row, index) => {
            if (index >= startIndex && index < endIndex) {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        });
    };

    // Handling pagination and display for the first table
    const processTable = document.getElementById('process-table');
    const processEntriesPerPageSelect = document.querySelectorAll('.entries-process');
    const processSearchInput = document.querySelectorAll('.search-process');
    const processPrevButtons = document.querySelectorAll('.prev-btn-process');
    const processNextButtons = document.querySelectorAll('.next-btn-process');

    const handleProcessPagination = (tableRows, currentPage, rowsPerPage) => {
        const totalPages = Math.ceil(tableRows.length / rowsPerPage);

        processPrevButtons.forEach(prevButton => {
            prevButton.addEventListener('click', function() {
                if (currentPage > 1) {
                    currentPage--;
                    showPage(tableRows, currentPage, rowsPerPage);
                }
            });
        });

        processNextButtons.forEach(nextButton => {
            nextButton.addEventListener('click', function() {
                if (currentPage < totalPages) {
                    currentPage++;
                    showPage(tableRows, currentPage, rowsPerPage);
                }
            });
        });
    };

    processEntriesPerPageSelect.forEach(entriesPerPage => {
        entriesPerPage.addEventListener('change', function() {
            const rowsPerPage = parseInt(this.value);
            const currentPage = 1;
            const processTableRows = processTable.querySelectorAll('tbody tr');
            showPage(processTableRows, currentPage, rowsPerPage);
            handleProcessPagination(processTableRows, currentPage, rowsPerPage);
        });
    });

    processSearchInput.forEach(input => {
        input.addEventListener('input', function() {
            const searchText = this.value.toLowerCase();
            let visibleRows = 0;
            const rowsPerPage = parseInt(processEntriesPerPageSelect[0].value);
            const processTableRows = processTable.querySelectorAll('tbody tr');

            processTableRows.forEach(row => {
                const rowData = row.textContent.toLowerCase();
                if (rowData.includes(searchText) && visibleRows < rowsPerPage) {
                    row.style.display = 'table-row';
                    visibleRows++;
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    const processRowsPerPage = parseInt(processEntriesPerPageSelect[0].value);
    const processCurrentPage = 1;
    const initialProcessTableRows = processTable.querySelectorAll('tbody tr');
    showPage(initialProcessTableRows, processCurrentPage, processRowsPerPage);
    handleProcessPagination(initialProcessTableRows, processCurrentPage, processRowsPerPage);

    // Handling pagination and display for the second table
    const processedTable = document.getElementById('processed-table');
    const processedEntriesPerPageSelect = document.querySelectorAll('.entries-processed');
    // ... (similar logic as above for the second table)
});
