$(document).ready(function () {
  // Fetch meal data and initialize DataTable
  $.ajax({
      url: "/nutrition/meals-and-foods/get-all-meals",
      method: "GET",
      success: function (response) {
          // Assuming 'response.meals' is the array of meals
          $('#mealsTableModal').DataTable({
              data: response.meals,
              columns: [
                  { data: "name" },
                  { 
                      data: "food_items",
                      render: function (data) {
                          // Concatenate food item names and serving counts
                          return data.map(item => `${item.name} (${item.serving_count} servings)`).join(', ');
                      }
                  },
                  { 
                      data: "id",
                      render: function (data) {
                          // Render action buttons for each meal
                          return `<button type="button" class="btn btn-info show-macros-btn" data-id="${data}">Show Macros</button>
                                  <button type="button" class="btn btn-primary edit-meal-btn" data-id="${data}">Edit</button>
                                  <button type="button" class="btn btn-danger delete-meal-btn" data-id="${data}">Delete</button>`;
                      }
                  }
              ],
              destroy: true // Allows reinitialization if called multiple times
          });
      },
      error: function (error) {
          console.log("Error fetching meals: " + error.responseText);
      }
  });

  // Rest of your JavaScript code for handling events
});
