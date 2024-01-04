$(document).ready(function () {
    $(".table").DataTable();
  });

  $(".edit-btn").on("click", function () {
    var foodId = $(this).data("id");

    // AJAX request to get food data
    $.ajax({
      url: "/nutrition/meals-and-foods/get-food/" + foodId,
      method: "GET",
      success: function (food) {
        // Populating the modal fields with the food item's data
        $("#editFoodId").val(food.id);
        $("#editName").val(food.name);
        $("#editServingSize").val(food.serving_size);
        $("#editCalories").val(food.calories);
        $("#editTotalFat").val(food.total_fat);
        $("#editTotalCarbohydrate").val(food.total_carbohydrate);
        $("#editTotalSugars").val(food.total_sugars);
        $("#editTotalProtein").val(food.total_protein);

        // Showing the modal
        $("#editFoodModal").modal("show");
      },
      error: function () {
        alert("Error fetching food item data");
      },
    });
  });

  $("#editFoodForm").on("submit", function (e) {
    e.preventDefault();

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

    $.ajax({
      url: "/nutrition/meals-and-foods/edit-food/" + updatedData.id,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(updatedData),
      success: function (response) {
        $("#editFoodModal").modal("hide");
        // Optionally, refresh the data on the page or display a success message
        location.reload(); // This will reload the page to reflect the changes
      },
      error: function () {
        alert("Error updating food item");
      },
    });
  });

  $(".delete-btn").on("click", function () {
    if(confirm("Are you sure you want to delete this food item?")) {
        var foodId = $(this).data("id");

        $.ajax({
            url: "/nutrition/meals-and-foods/delete-food/" + foodId,
            method: "POST",
            success: function (response) {
                alert("Food item deleted successfully");
                location.reload(); // Reload the page to reflect the changes
            },
            error: function () {
                alert("Error deleting food item");
            },
        });
    }
});
