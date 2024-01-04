$(document).ready(function () {
    // Initialize DataTables
    var table = $("#foodItemsTable").DataTable();

  });

  $(document).ready(function () {
    $(".food-item-checkbox").change(function () {
      var servingInput = $(this).closest("tr").find(".serving-count-input");
      if ($(this).is(":checked")) {
        servingInput.show();
      } else {
        servingInput.hide().val(""); // Hide and clear the input
      }
    });

    $("#createMealForm").on("submit", function (e) {
      e.preventDefault();

      var mealName = $("#mealName").val();
      var mealData = {
        name: mealName,
        food_items: [],
      };

      $(".food-item-checkbox:checked").each(function () {
    var foodId = $(this).val();
    var servingCount = $(this).closest("tr").find(".serving-count-input").val();
    mealData.food_items.push({ id: foodId, serving_count: servingCount });
});


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