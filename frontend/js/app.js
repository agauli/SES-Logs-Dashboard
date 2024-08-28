document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('logForm');
    const resultsContent = document.getElementById('results-content');
    const loadingIndicator = document.getElementById('loading-indicator');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const logGroup = document.getElementById('log-group').value;
        const startDate = formatDate(document.getElementById('start-date').value);
        const endDate = formatDate(document.getElementById('end-date').value);
        const eventType = document.getElementById('event-type').value;

        const url = `http://127.0.0.1:5000/api/get_ses_logs?log-group=${encodeURIComponent(logGroup)}&start-date=${encodeURIComponent(startDate)}&end-date=${encodeURIComponent(endDate)}&event-type=${encodeURIComponent(eventType)}`;

        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultsContent.innerHTML = '';  // Clear previous results

        try {
            const response = await fetch(url);
            const data = await response.json();
            
            displayResults(data);
        } catch (error) {
            resultsContent.innerHTML = '<p>Error fetching data. Please try again later.</p>';
        } finally {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
        }
    });

    function formatDate(dateInput) {
        // Convert input date format YYYY-MM-DD to YYYY/MM/DD
        const [year, month, day] = dateInput.split('-');
        return `${year}/${month}/${day}`;
    }

    function displayResults(data) {
        resultsContent.innerHTML = '';

        for (const [key, value] of Object.entries(data)) {
            if (value.length > 0) {
                const section = document.createElement('section');
                section.innerHTML = `<h3>${key.replace('_', ' ').toUpperCase()}</h3>`;
                
                const table = document.createElement('table');

                // Create the table header with filter inputs
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');
                Object.keys(value[0]).forEach(header => {
                    const th = document.createElement('th');
                    th.innerHTML = `${header}<br><input type="text" class="filter" placeholder="Filter ${header}">`;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create the table body
                const tbody = document.createElement('tbody');
                value.forEach(item => {
                    const row = document.createElement('tr');
                    Object.values(item).forEach(val => {
                        const td = document.createElement('td');
                        td.textContent = val;
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);

                // Add the table to the section
                section.appendChild(table);
                resultsContent.appendChild(section);

                // Add filtering functionality
                const filters = section.querySelectorAll('.filter');
                filters.forEach((filter, index) => {
                    filter.addEventListener('input', () => {
                        const filterValue = filter.value.toLowerCase();
                        const rows = tbody.querySelectorAll('tr');
                        rows.forEach(row => {
                            const cell = row.cells[index];
                            if (cell) {
                                const cellText = cell.textContent.toLowerCase();
                                row.style.display = cellText.includes(filterValue) ? '' : 'none';
                            }
                        });
                    });
                });
            }
        }
    }
});
