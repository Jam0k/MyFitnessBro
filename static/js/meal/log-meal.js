$(document).ready(function() {
    var selectedMealId = null;

    // Fetch and populate meals in DataTables
    $.ajax({
        url: '/nutrition/meals-and-foods/get-all-meals',
        method: 'GET',
        success: function(response) {
            var table = $('#mealsTable').DataTable({
                data: response.meals,
                columns: [
                    { data: 'name' },
                    { data: 'food_items', render: function(data) {
                        return data.map(item => `${item.name} (${item.serving_count} servings)`).join(', ');
                    }},
                    { data: 'id', render: function(data) {
                        return `<button class="btn btn-primary select-meal-btn" data-id="${data}">Select</button>`;
                    }}
                ]
            });

            // Handle meal selection from table
            $('#mealsTable tbody').on('click', '.select-meal-btn', function() {
                var mealId = $(this).data('id');
                
                // Check if the clicked meal is already selected
                if (selectedMealId === mealId) {
                    // If already selected, de-select it
                    selectedMealId = null;
                    $('#selectedMealId').val('');
                    table.$('tr.selected').removeClass('selected');
                    $('.select-meal-btn').prop('disabled', false);
                    $('#selectedMealDisplay').text('');
                } else {
                    // Select new meal
                    selectedMealId = mealId;
                    $('#selectedMealId').val(mealId);

                    // Highlight the selected row and disable other select buttons
                    table.$('tr.selected').removeClass('selected');
                    $(this).closest('tr').addClass('selected');
                    $('.select-meal-btn').not(this).prop('disabled', true);

                    // Display the selected meal name
                    var selectedMealName = table.row($(this).parents('tr')).data().name;
                    $('#selectedMealDisplay').text('Selected Meal: ' + selectedMealName);
                }
            });
        },
        error: function(error) {
            console.log('Error fetching meals: ' + error.responseText);
        }
    });

    // Handle form submission for logging a meal
    $("#logMealForm").on("submit", function(e) {
        e.preventDefault();
        if (!selectedMealId) {
            alert("Please select a meal first.");
            return;
        }

        var mealType = $("#mealType").val();
        var logDate = $("#logDate").val();

        var logData = {
            meal_id: selectedMealId,
            meal_type: mealType,
            log_date: logDate
        };

        // AJAX request to log the meal
        $.ajax({
            url: "/nutrition/meals-and-foods/log-meal",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(logData),
            success: function(response) {
                alert("Meal logged successfully");
            },
            error: function(error) {
                alert("Error logging meal: " + error.responseText);
            }
        });
    });
});
