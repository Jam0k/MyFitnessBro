$(document).ready(function () {
    var mealData = { food_items: {} };

    // Function to populate the food items table
    function populateFoodItemsTable() {
        $.ajax({
            url: "/nutrition/browse-food", // Adjust the endpoint as necessary
            method: "GET",
            success: function (response) {
                $('#foodItemsTableModal').DataTable({
                    data: response,
                    destroy: true, // Allows reinitialization
                    columns: [
                        {
                            data: null,
                            render: function (data, type, row) {
                                return `<input type="checkbox" class="food-item-checkbox" value="${row.id}" id="foodItemModal${row.id}" />
                                        <label for="foodItemModal${row.id}">${row.name} (Serving Size: ${row.serving_size}g)</label>`;
                            }
                        },
                        {
                            data: null,
                            render: function () {
                                return `<input type="number" min="0" step="any" class="form-control serving-count-input" placeholder="Serving count" style="display: none" />`;
                            }
                        }
                    ]
                });
            },
            error: function (error) {
                console.log("Error fetching food items: " + error.responseText);
            }
        });
    }

    populateFoodItemsTable();

    // Delegate checkbox change event to the DataTable
    $('#foodItemsTableModal tbody').on('change', '.food-item-checkbox', function () {
        var foodId = $(this).val();
        var servingInput = $(this).closest("tr").find(".serving-count-input");

        if ($(this).is(":checked")) {
            servingInput.show();
            mealData.food_items[foodId] = { id: foodId, serving_count: servingInput.val() || 0 };
        } else {
            servingInput.hide().val("");
            delete mealData.food_items[foodId];
        }
    });

    // Update serving count in meal data
    $('#foodItemsTableModal tbody').on('change', '.serving-count-input', function () {
        var foodId = $(this).closest("tr").find(".food-item-checkbox").val();
        if (mealData.food_items[foodId]) {
            mealData.food_items[foodId].serving_count = $(this).val() || 0;
        }
    });

    // Handle form submission for creating a new meal
    $("#createMealForm").on("submit", function (e) {
        e.preventDefault();

        var mealName = $("#mealNameModal").val(); // Ensure this ID matches your input field in the modal
        var formData = {
            name: mealName,
            food_items: Object.values(mealData.food_items)
        };

        $.ajax({
            url: "/nutrition/meals-and-foods/create-new-meal",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                alert("Meal created successfully");
                $('#createMealModal').modal('hide'); // Hide the modal after success
            },
            error: function () {
                alert("Error creating meal");
            },
        });
    });
});
