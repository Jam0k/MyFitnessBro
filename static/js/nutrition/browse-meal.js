$(document).ready(function () {
    // Fetch meal data and initialize DataTable
    var mealsTableModal; // Declare it globally so it can be used in delete logic
    $.ajax({
        url: "/nutrition/meals-and-foods/get-all-meals",
        method: "GET",
        success: function (response) {
            mealsTableModal = $('#mealsTableModal').DataTable({
                data: response.meals,
                columns: [
                    { data: "name" },
                    {
                        data: "food_items",
                        render: function (data) {
                            return data.map(item => `${item.name} (${item.serving_count} servings)`).join(', ');
                        }
                    },
                    {
                        data: "id",
                        render: function (data) {
                            return `<button type="button" class="btn btn-info show-macros-btn" data-id="${data}">Show Macros</button>
                                    <button type="button" class="btn btn-primary edit-meal-btn" data-id="${data}">Edit</button>
                                    <button type="button" class="btn btn-danger delete-meal-btn" data-id="${data}">Delete</button>`;
                        }
                    }
                ],
                destroy: true
            });
        },
        error: function (error) {
            console.log("Error fetching meals: " + error.responseText);
        }
    });

    let deletedFoodItemIds = []; // Array to keep track of deleted food items

    // Delete meal
    $('#mealsTableModal').on('click', '.delete-meal-btn', function () {
        var mealId = $(this).data("id");
        if (confirm("Are you sure you want to delete this meal?")) {
            $.ajax({
                url: "/nutrition/meals-and-foods/delete-meal/" + mealId,
                method: "POST",
                success: function () {
                    alert("Meal deleted successfully");
                    mealsTableModal.row($(this).parents('tr')).remove().draw(); // Remove the row from DataTable
                },
                error: function (xhr) {
                    alert("Error deleting meal: " + xhr.responseText);
                }
            });
        }
    });

    // Edit meal
    $('#mealsTableModal').on('click', '.edit-meal-btn', function () {
        var mealId = $(this).data("id");
        $("#editMealModal").data("meal-id", mealId);
        $.ajax({
            url: "/nutrition/meals-and-foods/get-meal/" + mealId,
            method: "GET",
            success: function (mealData) {
                populateEditModal(mealData);
                $("#editMealModal").modal("show");
                fetchFoodItemsForDropdown();
            },
            error: function () {
                alert("Error fetching meal data for editing");
            },
        });
    });

    // Function to populate the edit meal modal
    function populateEditModal(mealData) {
        $("#editMealName").val(mealData.name);
        var foodItemsList = $("#editFoodItemsList");
        foodItemsList.empty(); // Clear existing items

        mealData.food_items.forEach(function (item) {
            var foodItemHtml = `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        ${item.name} (Serving Size: ${item.serving_size})
                        <input type="number" class="form-control ml-2" style="width: 80px;" 
                               value="${item.serving_count}" step="0.01" data-food-id="${item.id}">
                    </div>
                </div>`;
            foodItemsList.append(foodItemHtml);
        });
    }

    // Handle form submission for editing a meal
    $("#editMealForm").on("submit", function (e) {
        e.preventDefault();
        var mealId = $("#editMealModal").data("meal-id");
        var updatedMealName = $("#editMealName").val();
        var updatedFoodItems = [];

        $("#editFoodItemsList input[type='number']").each(function () {
            updatedFoodItems.push({
                id: $(this).data("food-id"),
                serving_count: parseFloat($(this).val())
            });
        });

        var updatedMealData = {
            name: updatedMealName,
            food_items: updatedFoodItems,
            deleted_food_items: deletedFoodItemIds
        };

        // AJAX call to update the meal
        $.ajax({
            url: "/nutrition/meals-and-foods/update-meal/" + mealId,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(updatedMealData),
            success: function () {
                alert("Meal updated successfully");
                $("#editMealModal").modal("hide");
                deletedFoodItemIds = []; // Reset the array
                // Refresh the data in the DataTable or update the UI as needed
            },
            error: function (xhr) {
                alert("Error updating meal: " + xhr.responseText);
            }
        });
    });

    // Fetch food items for dropdown
    function fetchFoodItemsForDropdown() {
        // Your code to fetch food items...
    }

    // Handle delete button click for existing food items in edit modal
    $("#editMealContent").on("click", ".delete-existing-food-item-btn", function () {
        var row = $(this).closest(".existing-food-item-row");
        var foodId = row.data("food-id");
        if (confirm("Are you sure you want to remove this item from the meal?")) {
            deletedFoodItemIds.push(foodId);
            row.fadeOut(300, function () {
                $(this).remove();
            });
        }
    });

    // Other event handlers or functions...
});
