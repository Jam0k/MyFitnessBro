$(document).ready(function() {
    // Handle the form submission
    $("#logFoodForm").on("submit", function(e) {
        e.preventDefault();

        // Gather data from the form
        var foodItemId = $("#foodItemSelector").val();
        var servingCount = $("#servingCount").val();
        var logDate = $("#logDate").val();
        var mealType = $("#mealType").val();

        // Construct the data object to be sent
        var logData = {
            food_item_id: foodItemId,
            serving_count: servingCount,
            log_date: logDate,
            meal_type: mealType
        };

        // AJAX request to log the food item
        $.ajax({
            url: "/nutrition/meals-and-foods/log-food",  // Replace with your actual endpoint
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(logData),
            success: function(response) {
                // Handle success - for example, display a success message or redirect
                alert("Food logged successfully");
            },
            error: function(error) {
                // Handle error - for example, display an error message
                alert("Error logging food: " + error.responseText);
            }
        });
    });

    // Optionally, populate the foodItemSelector dropdown with food items from the server
    // This part of the code can be modified or expanded based on how you're fetching the food items
    $.ajax({
        url: "/nutrition/meals-and-foods/get-all-food-items",  // Replace with your actual endpoint
        method: "GET",
        success: function(foodItems) {
            foodItems.forEach(function(foodItem) {
                $("#foodItemSelector").append(new Option(foodItem.name, foodItem.id));
            });
        },
        error: function(error) {
            alert("Error fetching food items");
        }
    });
});
