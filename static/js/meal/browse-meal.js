$(document).ready(function () {
  $("#mealsTable").DataTable();

  let deletedFoodItemIds = []; // Array to keep track of deleted food items

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

let deletedFoodItemIds = []; // Array to keep track of deleted food items

// Delete button for existing food items
$("#editMealContent").on(
  "click",
  ".delete-existing-food-item-btn",
  function () {
    var row = $(this).closest(".existing-food-item-row");
    var foodId = row.data("food-id");
    if (confirm("Are you sure you want to remove this item from the meal?")) {
      deletedFoodItemIds.push(foodId);
      row.fadeOut(300, function () {
        $(this).remove();
      });
    }
  }
);

function populateEditModal(mealData) {
  var editContent = $("#editMealContent");
  editContent.empty(); // Clear existing content

  var htmlContent = `
        <div class="form-group">
            <label><b>Meal Name</b></label>
            <input type="text" class="form-control" id="editMealName" value="${mealData.name}">
        </div>
        <div class="form-group">
            <label><b>Current Food Items</b></label>
            <ul class="list-group mb-3">`;

  mealData.food_items.forEach((foodItem) => {
    htmlContent += `
            <li class="list-group-item d-flex justify-content-between align-items-center existing-food-item-row" data-food-id="${foodItem.id}">
                ${foodItem.name}
                <div>
                <input type="number" class="form-control mr-2" style="width: 80px; display: inline-block;" value="${foodItem.serving_count}" step="0.01">
                <button type="button" class="btn btn-danger btn-sm delete-existing-food-item-btn">Delete</button>
                </div>
            </li>`;
  });

  htmlContent += `
            </ul>
            <label><b>Add New Food Item</b></label>
            <div class="input-group mb-3">
                <select id="foodItemSelector" class="form-control"></select>
                <div class="input-group-append">
                    <button type="button" class="btn btn-success" id="addFoodItemBtn">Add</button>
                </div>
            </div>
            <div id="newFoodItemsList" class="list-group"></div>`;

  editContent.html(htmlContent);
}

// Handle delete button click for existing food items
$("#editMealContent").on(
  "click",
  ".delete-existing-food-item-btn",
  function () {
    $(this).closest(".existing-food-item-row").remove();
    // Potentially mark this item for deletion in the database
  }
);

$("#mealsTable").on("click", ".show-macros-btn", function () {
  var mealId = $(this).data("id");

  $.ajax({
    url: "/nutrition/meals-and-foods/get-macros/" + mealId,
    method: "GET",
    success: function (response) {
      // Render Chart
      var ctx = document.getElementById("macrosPieChart").getContext("2d");
      new Chart(ctx, {
        type: "pie",
        data: response.chartData,
        options: {
          // Options here if needed
        },
      });

            // Initialize totals
            var totalCalories = 0, totalFat = 0, totalCarbs = 0, totalSugars = 0, totalProtein = 0;

            // Render Table
            var tableHtml = "<table class='table'><thead><tr><th>Food Item</th><th>Calories</th><th>Fat (g)</th><th>Carbs (g)</th><th>Sugars (g)</th><th>Protein (g)</th></tr></thead><tbody>";
            response.tableData.forEach(function(item) {
                tableHtml += `<tr><td>${item.name}</td><td>${item.calories}</td><td>${item.fat}</td><td>${item.carbs}</td><td>${item.sugars}</td><td>${item.protein}</td></tr>`;
                
                // Accumulate totals
                totalCalories += item.calories;
                totalFat += item.fat;
                totalCarbs += item.carbs;
                totalSugars += item.sugars;
                totalProtein += item.protein;
            });

            // Add totals row
            tableHtml += `<tr><th>Total</th><td>${totalCalories.toFixed(1)}</td><td>${totalFat.toFixed(1)}</td><td>${totalCarbs.toFixed(1)}</td><td>${totalSugars.toFixed(1)}</td><td>${totalProtein.toFixed(1)}</td></tr>`;
            tableHtml += "</tbody></table>";

            $("#macrosContent").html(tableHtml);
            $("#macrosModal").modal("show");
        },
        error: function () {
            alert("Error fetching nutritional information");
        }
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

// Add button for new food items
$("#editMealContent").on("click", "#addFoodItemBtn", function () {
  var selectedFoodId = $("#foodItemSelector").val();
  var alreadyAdded =
    $("#newFoodItemsList").find(`[data-food-id="${selectedFoodId}"]`).length >
    0;

  if (alreadyAdded) {
    alert("This food item has already been added.");
    return;
  }

  var selectedFoodText = $("#foodItemSelector option:selected").text();
  var newItemHtml = `
          <li class="list-group-item d-flex justify-content-between align-items-center food-item-row" data-food-id="${selectedFoodId}">
              ${selectedFoodText}
              <div>
                  <input type="number" class="form-control mr-2" style="width: 80px; display: inline-block;" value="1">
                  <button type="button" class="btn btn-danger btn-sm remove-food-item-btn">Remove</button>
              </div>
          </li>`;
  $("#newFoodItemsList").append(newItemHtml);
});

// Remove button for new food items
$("#editMealContent").on("click", ".remove-food-item-btn", function () {
  $(this)
    .closest(".food-item-row")
    .fadeOut(300, function () {
      $(this).remove();
    });
});

$("#editMealForm").on("submit", function (e) {
  e.preventDefault();

  var mealId = $("#editMealModal").data("meal-id");
  var updatedMealName = $("#editMealName").val();
  var foodItems = [];

  // Get serving count for existing food items
  $(".existing-food-item-row").each(function () {
    var foodId = $(this).data("food-id");
    var servingCount = $(this).find('input[type="number"]').val();
    foodItems.push({ id: foodId, serving_count: parseFloat(servingCount) });
  });

  // Get serving count for newly added food items
  $(".food-item-row").each(function () {
    var foodId = $(this).data("food-id");
    var servingCount = $(this).find('input[type="number"]').val();
    foodItems.push({ id: foodId, serving_count: parseFloat(servingCount) });
  });

  var updatedMealData = {
    name: updatedMealName,
    food_items: foodItems,
    deleted_food_items: deletedFoodItemIds, // Include deleted food items
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
    error: function (xhr) {
      alert("Error updating meal: " + xhr.responseText);
    },
  });
});