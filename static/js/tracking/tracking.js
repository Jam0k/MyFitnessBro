$(document).ready(function () {
    // Set the date input to the selected date from the server
    $('#dateFilter').val(selectedDate);

    // Event listener for date change
    $('#dateFilter').on('change', function() {
        var newSelectedDate = $(this).val();
        window.location.href = '/nutrition/tracking?date=' + newSelectedDate;
    });
        // Loop through each table with an ID that starts with 'mealTypeTable'
    $("table[id^='mealTypeTable']").each(function () {
        // Initialize DataTables on each table
        $(this).DataTable();
    });
    
});


document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('grandTotalPieChart').getContext('2d');

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
            // You can add more options here if needed
        }
    });
});

