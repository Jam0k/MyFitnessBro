$(document).ready(function() {
    // Handle the form submission for logging a meal
    $("#logMealForm").on("submit", function(e) {
        e.preventDefault();

        // Gather data from the form
        var mealId = $("#mealSelector").val();
        var mealType = $("#mealType").val();
        var logDate = $("#logDate").val();

        // Construct the data object to be sent
        var logData = {
            meal_id: mealId,
            meal_type: mealType,
            log_date: logDate
        };

        // AJAX request to log the meal
        $.ajax({
            url: "/nutrition/meals-and-foods/log-meal",  // Replace with your actual endpoint
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(logData),
            success: function(response) {
                // Handle success
                alert("Meal logged successfully");
            },
            error: function(error) {
                // Handle error
                alert("Error logging meal: " + error.responseText);
            }
        });
    });

    // Optionally, populate the mealSelector dropdown with meals from the server
    // This part of the code can be modified based on how you're fetching the meals
    $.ajax({
        url: "/nutrition/meals-and-foods/get-all-meals",  // Replace with your actual endpoint
        method: "GET",
        success: function(meals) {
            meals.forEach(function(meal) {
                $("#mealSelector").append(new Option(meal.name, meal.id));
            });
        },
        error: function(error) {
            alert("Error fetching meals");
        }
    });
});
