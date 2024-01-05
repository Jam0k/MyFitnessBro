$(document).ready(function () {
  // Initialize DataTables for the food items table
  var table = $("#foodItemsTable").DataTable();

  // Event handler for checkbox changes in the food items table
  $(".food-item-checkbox").change(function () {
      var servingInput = $(this).closest("tr").find(".serving-count-input");
      if ($(this).is(":checked")) {
          // Show the serving count input if checkbox is checked
          servingInput.show();
      } else {
          // Hide and clear the input if checkbox is unchecked
          servingInput.hide().val("");
      }
  });

  // Form submission event for creating a new meal
  $("#createMealForm").on("submit", function (e) {
      e.preventDefault();

      // Collecting meal name and food items data
      var mealName = $("#mealName").val();
      var mealData = {
          name: mealName,
          food_items: []
      };

      // Loop through each checked food item and collect its data
      $(".food-item-checkbox:checked").each(function () {
          var foodId = $(this).val();
          var servingCount = $(this).closest("tr").find(".serving-count-input").val();
          mealData.food_items.push({ id: foodId, serving_count: servingCount });
      });

      // AJAX request to create a new meal
      $.ajax({
          url: "/nutrition/meals-and-foods/create-new-meal",
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify(mealData),
          success: function (response) {
              alert("Meal created successfully");
              // Redirect or update UI as needed
          },
          error: function () {
              alert("Error creating meal");
          },
      });
  });
});
