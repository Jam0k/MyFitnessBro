$(document).ready(function () {
    // Set the initial date inputs to the selected date from the server
    $('#startDateFilter').val(selectedStartDate);
    $('#endDateFilter').val(selectedEndDate);

    // Event listener for start date change
    $('#startDateFilter').on('change', function() {
        updateDateFilter();
    });

    // Event listener for end date change
    $('#endDateFilter').on('change', function() {
        updateDateFilter();
    });

    function updateDateFilter() {
        var newStartDate = $('#startDateFilter').val();
        var newEndDate = $('#endDateFilter').val();
        window.location.href = '/nutrition/?start_date=' + newStartDate + '&end_date=' + newEndDate;
    }

    // Initialize DataTables on tables with IDs starting with 'mealTypeTable'
    $("table[id^='mealTypeTable']").each(function () {
        $(this).DataTable();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var grandTotalPieChartElement = document.getElementById('grandTotalPieChart');

    if (grandTotalPieChartElement) {
        var ctx = grandTotalPieChartElement.getContext('2d');

        // Remove 'calories' from the grandTotalData
        delete grandTotalData.calories;

        // Prepare the labels and data arrays
        var labels = Object.keys(grandTotalData);
        var dataValues = Object.values(grandTotalData);

        var chartData = {
            labels: labels,
            datasets: [{
                label: 'Grand Totals',
                data: dataValues,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        };

        new Chart(ctx, {
            type: 'pie',
            data: chartData,
            options: {
                responsive: true
                // Add more options here if needed
            }
        });
    }
});
