document.addEventListener('DOMContentLoaded', function() {
    // Initialize Flatpickr for date inputs
    const startDate = flatpickr("#start-date", {
        dateFormat: "Y-m-d",
    });
    
    const endDate = flatpickr("#end-date", {
        dateFormat: "Y-m-d",
    });

    // Function to set date range
    function setDateRange(start, end) {
        startDate.setDate(start);
        endDate.setDate(end);
    }

    // Quick select buttons
    document.getElementById('today').addEventListener('click', function() {
        const today = new Date();
        setDateRange(today, today);
    });

    document.getElementById('yesterday').addEventListener('click', function() {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        setDateRange(yesterday, yesterday);
    });

    document.getElementById('last7days').addEventListener('click', function() {
        const end = new Date();
        const start = new Date();
        start.setDate(start.getDate() - 6);
        setDateRange(start, end);
    });

    document.getElementById('lastMonth').addEventListener('click', function() {
        const today = new Date();
        const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
        const lastDayOfLastMonth = new Date(today.getFullYear(), today.getMonth(), 0);
        setDateRange(lastMonth, lastDayOfLastMonth);
    });

    document.getElementById('weekToDate').addEventListener('click', function() {
        const today = new Date();
        const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay()));
        setDateRange(startOfWeek, new Date());
    });

    document.getElementById('monthToDate').addEventListener('click', function() {
        const today = new Date();
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
        setDateRange(startOfMonth, today);
    });

    // Apply button
    document.getElementById('apply').addEventListener('click', function() {
        console.log('Start Date:', startDate.selectedDates[0]);
        console.log('End Date:', endDate.selectedDates[0]);
        // Fetch data from Django backend
        fetchData(startDate.input.value, endDate.input.value);
    });

    // Function to fetch data using AJAX
    function fetchData(startDate, endDate) {
        // Show loading indicator
        document.getElementById('results-container').innerHTML = 'Loading...';

        // Construct URL with query parameters
        const url = `/pos/load_result/?start_date=${startDate}&end_date=${endDate}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(data => {
            // Update the results container with the fetched data
            document.getElementById('results-container').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results-container').innerHTML = 'An error occurred while fetching data.';
        });
    }

    // Attach fetchData to quick select buttons
    document.querySelectorAll('.quick-select button').forEach(button => {
        button.addEventListener('click', function() {
            // Small delay to ensure the date inputs are updated before fetching
            setTimeout(() => {
                fetchData(startDate.input.value, endDate.input.value);
            }, 100);
        });
    });
});
