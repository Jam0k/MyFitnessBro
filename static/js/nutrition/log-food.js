$(document).ready(function() {
    var selectedFoodItemId = null;

    // Set default date to today
    var today = new Date().toISOString().split('T')[0];
    $('#logDate').val(today);

    // Fetch and populate food items in DataTables
    $.ajax({
        url: 'get-all-food-items', // Replace with your actual endpoint
        method: 'GET',
        success: function(response) {
            var table = $('#foodItemsTable').DataTable({
                data: response, // Directly use the response array
                columns: [
                    { data: 'name' },
                    { data: 'serving_size' },
                    { data: 'calories' },
                    { data: 'total_protein' },
                    { data: 'total_carbohydrate' },
                    { data: 'total_sugars' },
                    { data: 'total_fat' },

                    { data: 'id', render: function(data) {
                        return `<button class="btn btn-primary select-food-item-btn" data-id="${data}">Select</button>`;
                    }}
                ]
            });

            // Handle food item selection from table
            $('#foodItemsTable tbody').on('click', '.select-food-item-btn', function() {
                var foodItemId = $(this).data('id');
                if(selectedFoodItemId === foodItemId) {
                    // Deselect the item
                    selectedFoodItemId = null;
                    $('#selectedFoodItemId').val('');
                    table.$('tr.selected').removeClass('selected');
                    $('.select-food-item-btn').prop('disabled', false);
                    $('#selectedFoodItemDisplay').text('');
                } else {
                    // Select new item
                    selectedFoodItemId = foodItemId;
                    $('#selectedFoodItemId').val(foodItemId);
                    table.$('tr.selected').removeClass('selected');
                    $(this).closest('tr').addClass('selected');
                    $('.select-food-item-btn').not(this).prop('disabled', true);
                    var selectedFoodItemName = table.row($(this).parents('tr')).data().name;
                    $('#selectedFoodItemDisplay').text('Selected Food Item: ' + selectedFoodItemName);
                }
            });
        },
        error: function(error) {
            console.log('Error fetching food items: ' + error.responseText);
        }
    });

    // Handle form submission for logging a food item
    $("#logFoodForm").on("submit", function(e) {
        e.preventDefault();
        if (!selectedFoodItemId) {
            alert("Please select a food item first.");
            return;
        }

        var servingCount = $("#servingCount").val();
        var logDate = $("#logDate").val();
        var mealType = $("#mealType").val();

        var logData = {
            food_item_id: selectedFoodItemId,
            serving_count: servingCount,
            log_date: logDate,
            meal_type: mealType
        };

// AJAX request to log the food item
$.ajax({
    url: "/nutrition/log-food", // Replace with your actual endpoint
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(logData),
    success: function(response) {
        // Show success alert
        $('#logFoodAlert').show();

        // Hide the alert after 2 seconds (2000 milliseconds)
        setTimeout(function() {
            $('#logFoodAlert').hide();
        }, 2000);
    },
    error: function(error) {
        alert("Error logging food item: " + error.responseText);
    }
});
    });
});
