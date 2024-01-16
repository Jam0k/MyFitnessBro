$(document).ready(function () {
    var table = $("#workoutPlanTable").DataTable({
      ajax: "/fitness/exercises-and-workouts/get-workout-plans",
      columns: [
        { data: "name" },
        {
          data: "exercises",
          render: function (data, type, row) {
            return data.map((exercise) => exercise.name).join(", ");
          },
        },
        {
          data: "id",
          render: function (data, type, row) {
            return (
              '<button class="btn btn-primary edit-btn" data-id="' +
              data +
              '">Edit</button>' +
              '<button class="btn btn-danger delete-btn" data-id="' +
              data +
              '">Delete</button>'
            );
          },
          orderable: false,
        },
      ],
    });

    var allExercisesTableInitialized = false;

    // Use document-level event delegation for dynamically loaded content
    $(document).on("click", ".edit-btn", function () {
      var workoutPlanId = $(this).data("id");
      openEditModal(workoutPlanId);
    });

    function openEditModal(workoutPlanId) {
      $("#editWorkoutPlanModal").data("workoutPlanId", workoutPlanId);

      // Fetch workout plan details from the server
      $.ajax({
        url:
          "/fitness/exercises-and-workouts/get-workout-plan/" + workoutPlanId,
        type: "GET",
        success: function (response) {
          var formHtml =
            '<div class="mb-3"><label for="workoutPlanName" class="form-label">Workout Plan Name</label>' +
            '<input type="text" class="form-control" id="workoutPlanName" name="name" value="' +
            response.name +
            '"></div>';

          formHtml +=
            '<div class="mb-3"><label class="form-label">Exercises</label>';
          response.exercises.forEach(function (exercise) {
            formHtml +=
              '<div class="form-check">' +
              '<input class="form-check-input" type="checkbox" value="' +
              exercise.id +
              '" id="exercise' +
              exercise.id +
              '" name="exercises" checked>' +
              '<label class="form-check-label" for="exercise' +
              exercise.id +
              '">' +
              exercise.name +
              "</label></div>";
          });
          formHtml += "</div>";
          $("#editWorkoutPlanModal")
            .find("#editWorkoutPlanForm")
            .html(formHtml);

          // Manually show the modal
          $("#editWorkoutPlanModal").modal("show");
        },
        error: function (xhr, status, error) {
          console.error("Error fetching workout plan:", status, error);
        },
      });

      // Initialize or reload the allExercisesTable
      if (!allExercisesTableInitialized) {
        allExercisesTableInitialized = true;
        $("#allExercisesTable").DataTable({
          ajax: "/fitness/exercises-and-workouts/get-exercises",
          columns: [
            { data: "name" },
            { data: "sets" },
            { data: "reps" },
            { data: "weight_lifted" },
            {
              data: "id",
              render: function (data, type, row) {
                return (
                  '<input type="checkbox" class="exercise-select" value="' +
                  data +
                  '">'
                );
              },
              orderable: false,
            },
          ],
        });
      } else {
        $("#allExercisesTable").DataTable().ajax.reload();
      }
    }

    // Handle form submission for saving changes
    $("#saveWorkoutPlanChanges").click(function () {
      var workoutPlanId = $("#editWorkoutPlanModal").data("workoutPlanId");
      var selectedExerciseIds = $(
        '#editWorkoutPlanForm input[name="exercises"]:checked'
      )
        .map(function () {
          return $(this).val();
        })
        .get();

      // Add newly selected exercises from the DataTable
      var newExercises = $("#allExercisesTable .exercise-select:checked")
        .map(function () {
          return $(this).val();
        })
        .get();

      var editedData = {
        name: $("#workoutPlanName").val(),
        exercises: selectedExerciseIds.concat(newExercises),
      };

      $.ajax({
        url:
          "/fitness/exercises-and-workouts/update-workout-plan/" +
          workoutPlanId,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(editedData),
        success: function (response) {
          $("#editWorkoutPlanModal").modal("hide");
          table.ajax.reload();
        },
        error: function (xhr, status, error) {
          console.error("Error saving changes:", status, error);
        },
      });
    });

    // Event listener for Delete button
    $("#workoutPlanTable").on("click", ".delete-btn", function () {
      var workoutPlanId = $(this).data("id");
      if (confirm("Are you sure you want to delete this workout plan?")) {
        $.ajax({
          url:
            "/fitness/exercises-and-workouts/delete-workout-plan/" +
            workoutPlanId,
          type: "DELETE",
          success: function (response) {
            table.ajax.reload();
          },
          error: function (xhr, status, error) {
            console.error("Error deleting workout plan:", status, error);
          },
        });
      }
    });
  });