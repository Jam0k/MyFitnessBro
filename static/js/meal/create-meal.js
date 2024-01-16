$(document).ready(function () {
    var table = $("#foodItemsTable").DataTable();
    var mealData = { food_items: [] };

    // Delegate checkbox change event to the DataTable
    $('#foodItemsTable tbody').on('change', '.food-item-checkbox', function () {
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

    $('#foodItemsTable tbody').on('change', '.serving-count-input', function () {
        var foodId = $(this).closest("tr").find(".food-item-checkbox").val();
        mealData.food_items[foodId].serving_count = $(this).val();
    });

    $("#createMealForm").on("submit", function (e) {
        e.preventDefault();

        var mealName = $("#mealName").val();
        mealData.name = mealName;

        var formData = {
            name: mealData.name,
            food_items: Object.values(mealData.food_items)
        };

        $.ajax({
            url: "/nutrition/meals-and-foods/create-new-meal",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                alert("Meal created successfully");
            },
            error: function () {
                alert("Error creating meal");
            },
        });
    });
});
