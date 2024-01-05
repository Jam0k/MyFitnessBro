$(document).ready(function () {
  // Initialize DataTables for all tables with class 'table'
  $(".table").DataTable();
});

// Event listener for Edit button click
$(".edit-btn").on("click", function () {
  var foodId = $(this).data("id");

  // AJAX request to get food data for editing
  $.ajax({
      url: "/nutrition/meals-and-foods/get-food/" + foodId,
      method: "GET",
      success: function (food) {
          // Populate the modal fields with the food item's data
          $("#editFoodId").val(food.id);
          $("#editName").val(food.name);
          $("#editServingSize").val(food.serving_size);
          $("#editCalories").val(food.calories);
          $("#editTotalFat").val(food.total_fat);
          $("#editTotalCarbohydrate").val(food.total_carbohydrate);
          $("#editTotalSugars").val(food.total_sugars);
          $("#editTotalProtein").val(food.total_protein);

          // Show the edit food modal
          $("#editFoodModal").modal("show");
      },
      error: function () {
          alert("Error fetching food item data");
      },
  });
});

// Event listener for Edit Food form submission
$("#editFoodForm").on("submit", function (e) {
  e.preventDefault();

  // Prepare the updated food item data
  var updatedData = {
      id: $("#editFoodId").val(),
      name: $("#editName").val(),
      serving_size: $("#editServingSize").val(),
      calories: $("#editCalories").val(),
      total_fat: $("#editTotalFat").val(),
      total_carbohydrate: $("#editTotalCarbohydrate").val(),
      total_sugars: $("#editTotalSugars").val(),
      total_protein: $("#editTotalProtein").val(),
  };

  // AJAX request to update the food item
  $.ajax({
      url: "/nutrition/meals-and-foods/edit-food/" + updatedData.id,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(updatedData),
      success: function (response) {
          // Hide the modal and reload the page to reflect changes
          $("#editFoodModal").modal("hide");
          location.reload();
      },
      error: function () {
          alert("Error updating food item");
      },
  });
});

// Event listener for Delete button click
$(".delete-btn").on("click", function () {
  if(confirm("Are you sure you want to delete this food item?")) {
      var foodId = $(this).data("id");

      // AJAX request to delete the food item
      $.ajax({
          url: "/nutrition/meals-and-foods/delete-food/" + foodId,
          method: "POST",
          success: function (response) {
              // Alert success and reload the page
              alert("Food item deleted successfully");
              location.reload();
          },
          error: function () {
              alert("Error deleting food item");
          },
      });
  }
});