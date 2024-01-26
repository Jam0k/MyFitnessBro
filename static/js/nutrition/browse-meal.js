$(document).ready(function () {
    var mealsTableModal;
    var editFoodItemsTable;
    var allFoodItemsTable;
    let deletedFoodItemIds = [];

    // Initialize the main meals list DataTable
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
                            return `
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

    // Delete meal
    $('#mealsTableModal').on('click', '.delete-meal-btn', function () {
        var mealId = $(this).data("id");
        if (confirm("Are you sure you want to delete this meal?")) {
            $.ajax({
                url: "/nutrition/meals-and-foods/delete-meal/" + mealId,
                method: "POST",
                success: function () {
                    alert("Meal deleted successfully");
                    mealsTableModal.row($(this).parents('tr')).remove().draw();
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
                fetchAllFoodItems();
                $("#editMealModal").modal("show");
            },
            error: function () {
                alert("Error fetching meal data for editing");
            },
        });
    });

    // Populate edit meal modal
    function populateEditModal(mealData) {
        $("#editMealName").val(mealData.name);
        deletedFoodItemIds = []; // Reset the array

        if ($.fn.DataTable.isDataTable('#editFoodItemsTable')) {
            $('#editFoodItemsTable').DataTable().clear().destroy();
        }
        editFoodItemsTable = $('#editFoodItemsTable').DataTable({
            data: mealData.food_items.map(item => ({
                name: item.name,
                serving_size: item.serving_size,
                serving_count: item.serving_count,
                actions: `<button type="button" class="btn btn-danger delete-food-item-btn" data-food-id="${item.id}">Delete</button>`
            })),
            columns: [
                { title: "Name", data: "name" },
                { title: "Serving Size", data: "serving_size" },
                { title: "Serving Count", data: "serving_count" },
                { title: "Actions", data: "actions" }
            ],
            destroy: true
        });
    }

    // Fetch all food items and initialize DataTable
    function fetchAllFoodItems() {
        $.ajax({
            url: "/nutrition/browse-food", // Adjust with your correct endpoint
            method: "GET",
            success: function (foodItems) {
                if ($.fn.DataTable.isDataTable('#allFoodItemsTable')) {
                    $('#allFoodItemsTable').DataTable().clear().destroy();
                }
                allFoodItemsTable = $('#allFoodItemsTable').DataTable({
                    data: foodItems,
                    columns: [
                        { title: "Name", data: "name" },
                        { title: "Serving Size", data: "serving_size" },
                        {
                            title: "Actions",
                            data: null,
                            defaultContent: "<button class='btn btn-primary add-food-item-btn'>Add</button>"
                        }
                    ],
                    destroy: true
                });
            },
            error: function (error) {
                console.log("Error fetching all food items: " + error.responseText);
            }
        });
    }

    // Handle form submission for editing a meal
    $("#editMealForm").on("submit", function (e) {
        e.preventDefault();
        var mealId = $("#editMealModal").data("meal-id");
        var updatedMealName = $("#editMealName").val();
        var updatedFoodItems = [];
    
        editFoodItemsTable.rows().every(function () {
            var row = this.data();
            var foodId = $(row.actions).data("food-id"); // Get the food ID
            var servingInput = $(this.node()).find('input').val(); // Extract the serving count value from the input
            var servingCount = servingInput ? parseFloat(servingInput) : 0; // Use 0 as default if input is empty or invalid
    
            updatedFoodItems.push({
                id: foodId,
                serving_count: servingCount
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
                // Refresh the data in the mealsTableModal or update the UI as needed
            },
            error: function (xhr) {
                alert("Error updating meal: " + xhr.responseText);
            }
        });
    });
    
    

    // Handle delete button click for existing food items in edit modal
    $(document).on('click', '.delete-food-item-btn', function () {
        var row = editFoodItemsTable.row($(this).parents('tr'));
        var foodId = $(this).data("food-id");
        deletedFoodItemIds.push(foodId);
        row.remove().draw();
    });

    // Handle add button click for food items in 'all food items' modal
    $(document).on('click', '.add-food-item-btn', function () {
        var foodItemData = allFoodItemsTable.row($(this).parents('tr')).data();
        editFoodItemsTable.row.add({
            name: foodItemData.name,
            serving_size: foodItemData.serving_size,
            serving_count: `<input type="number" class="form-control" style="width: 80px;" 
                            value="1" step="0.01" data-food-id="${foodItemData.id}">`,
            actions: `<button type="button" class="btn btn-danger delete-food-item-btn" data-food-id="${foodItemData.id}">Delete</button>`
        }).draw();
    }); 

    // Other event handlers or functions...
});
