$(document).ready(function () {
    $("#mealsTable").DataTable();

    // Bind click event to delete buttons dynamically
    $("#mealsTable").on("click", ".delete-meal-btn", function () {
      var mealId = $(this).data("id");
      console.log("Meal ID to delete:", mealId); // Debugging line
      if (confirm("Are you sure you want to delete this meal?")) {
        $.ajax({
          url: "/nutrition/meals-and-foods/delete-meal/" + mealId,
          method: "POST",
          success: function (response) {
            alert("Meal deleted successfully");
            location.reload(); // Reload the page to reflect the changes
          },
          error: function (xhr, status, error) {
            alert("Error deleting meal: " + xhr.responseText);
          },
        });
      }
    });
  });

  function populateEditModal(mealData) {
    var editContent = $("#editMealContent");
    editContent.empty(); // Clear existing content

    var htmlContent =
      '<div class="form-group"><label><b>Meal Name</b></label><input type="text" class="form-control" id="editMealName" value="' +
      mealData.name +
      '"></div>';
    htmlContent += '<div class="form-group"><label><b>Food Items</b></label>';

    mealData.food_items.forEach(function (foodItem) {
      htmlContent +=
        '<div class="row mb-2"><div class="col-8">' + foodItem.name + "</div>";
      htmlContent +=
        '<div class="col-4"><input type="number" class="form-control" value="' +
        foodItem.serving_count +
        '" data-food-id="' +
        foodItem.id +
        '"></div></div>';
    });

    // Dropdown for selecting food items
    htmlContent +=
      '<div class="form-group mt-3"><label><b>Add Food Item</b></label><div class="input-group">';
    htmlContent +=
      '<select id="foodItemSelector" class="form-control"></select>';
    htmlContent +=
      '<div class="input-group-append"><button type="button" class="btn btn-success" id="addFoodItemBtn">Add</button></div></div>';

    editContent.html(htmlContent);
  }

  $("#mealsTable").on("click", ".show-macros-btn", function () {
    var mealId = $(this).data("id");

    $.ajax({
      url: "/nutrition/meals-and-foods/get-macros/" + mealId,
      method: "GET",
      success: function (data) {
        // Populate the modal with data
        $("#macrosContent").html(data);
        $("#macrosModal").modal("show");
      },
      error: function () {
        alert("Error fetching nutritional information");
      },
    });
  });

  // Bind click event to edit buttons dynamically
  $("#mealsTable").on("click", ".edit-meal-btn", function () {
    var mealId = $(this).data("id");
    $("#editMealModal").data("meal-id", mealId);

    // AJAX request to fetch meal data for editing
    $.ajax({
      url: "/nutrition/meals-and-foods/get-meal/" + mealId,
      method: "GET",
      success: function (mealData) {
        populateEditModal(mealData);
        $("#editMealModal").modal("show");
        fetchFoodItemsForDropdown(); // Call this after the modal is shown
      },
      error: function () {
        alert("Error fetching meal data for editing");
      },
    });
  });

  function fetchFoodItemsForDropdown() {
    $.ajax({
      url: "/nutrition/meals-and-foods/get-all-food-items",
      method: "GET",
      success: function (data) {
        var dropdown = $("#foodItemSelector");
        dropdown.empty(); // Clear existing options

        data.forEach(function (item) {
          // Concatenate the item name and serving size
          var optionText =
            item.name + " (Serving Size: " + item.serving_size + "g)";
          dropdown.append(new Option(optionText, item.id));
        });
      },
      error: function () {
        alert("Error fetching food items");
      },
    });
  }

  // Handle the 'Add' button click
  $("#editMealContent").on("click", "#addFoodItemBtn", function () {
    var selectedFoodId = $("#foodItemSelector").val();
    var alreadyAdded =
      $("#editMealContent").find('[data-food-id="' + selectedFoodId + '"]')
        .length > 0;

    if (alreadyAdded) {
      alert("This food item has already been added.");
      return; // Prevent adding the duplicate item
    }

    var selectedFoodText = $("#foodItemSelector option:selected").text();

    // Append the selected food item to a list or table in the modal
    var newItemHtml =
      '<div class="row mb-2 food-item-row" data-food-id="' +
      selectedFoodId +
      '">';
    newItemHtml += '<div class="col-6">' + selectedFoodText + "</div>";
    newItemHtml +=
      '<div class="col-4"><input type="number" class="form-control serving-count" value="1"></div>'; // Default serving count as 1
    newItemHtml +=
      '<div class="col-2"><button type="button" class="btn btn-danger remove-food-item-btn">Remove</button></div>';
    newItemHtml += "</div>";
    $("#editMealContent").append(newItemHtml);
  });

  // Handle removing a food item
  $("#editMealContent").on("click", ".remove-food-item-btn", function () {
    $(this).closest(".food-item-row").remove();
  });

  $("#editMealForm").on("submit", function (e) {
    e.preventDefault();

    var mealId = $("#editMealModal").data("meal-id");
    var updatedMealName = $("#editMealName").val();
    var foodItems = [];

    // Get existing and newly added food items
    $(".food-item-row").each(function () {
      var foodId = $(this).data("food-id");
      var servingCount = $(this).find(".serving-count").val();
      foodItems.push({ id: foodId, serving_count: servingCount });
    });

    var updatedMealData = {
      name: updatedMealName,
      food_items: foodItems,
    };

    // AJAX call to update the meal
    $.ajax({
      url: "/nutrition/meals-and-foods/update-meal/" + mealId,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(updatedMealData),
      success: function (response) {
        alert("Meal updated successfully");
        $("#editMealModal").modal("hide");
        location.reload(); // Reload the page to reflect the changes
      },
      error: function () {
        alert("Error updating meal");
      },
    });
  });

  function collectUpdatedMealData() {
    // Code to collect updated meal data from the form...
    // This includes the meal name and updated food items and serving sizes
    return updatedMealData;
  }