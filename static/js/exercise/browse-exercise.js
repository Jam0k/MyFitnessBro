$(document).ready(function() {
    $('#exerciseTable').DataTable({
        ajax: '/fitness/exercises-and-workouts/get-exercises',
        columns: [
            { data: 'name' },
            { data: 'category' },
            { data: 'duration_minutes' },
            { data: 'sets' },
            { data: 'reps' },
            { data: 'weight_lifted' },
            { data: 'calories_burned' },
            { data: 'notes' },
            {
                data: 'id', // Use 'id' to create buttons
                render: function(data, type, row) {
                    // Create Edit and Delete buttons
                    return '<button class="btn btn-primary edit-btn" data-id="' + data + '">Edit</button>' +
                           '<button class="btn btn-danger delete-btn" data-id="' + data + '">Delete</button>';
                },
                orderable: false
            }
        ]
    });

// Event listener for Edit button
$('#exerciseTable').on('click', '.edit-btn', function() {
        var exerciseId = $(this).data('id');

        $.ajax({
            url: '/fitness/exercises-and-workouts/get-exercise/' + exerciseId,
            type: 'GET',
            success: function(response) {
                $('#editExerciseId').val(response.id);
                $('#editExerciseName').val(response.name);
                $('#editExerciseCategory').val(response.category);
                $('#editExerciseDuration').val(response.duration_minutes);
                $('#editExerciseSets').val(response.sets);
                $('#editExerciseReps').val(response.reps);
                $('#editExerciseWeight').val(response.weight_lifted);
                $('#editExerciseCalories').val(response.calories_burned);
                $('#editExerciseNotes').val(response.notes);

                $('#editExerciseModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error fetching exercise:', status, error);
            }
        });
    });

    $('#saveExerciseChanges').click(function() {
        var exerciseId = $('#editExerciseId').val();
        var updatedData = {
            name: $('#editExerciseName').val(),
            category: $('#editExerciseCategory').val(),
            duration_minutes: $('#editExerciseDuration').val(),
            sets: $('#editExerciseSets').val(),
            reps: $('#editExerciseReps').val(),
            weight_lifted: $('#editExerciseWeight').val(),
            calories_burned: $('#editExerciseCalories').val(),
            notes: $('#editExerciseNotes').val()
        };

        $.ajax({
            url: '/fitness/exercises-and-workouts/update-exercise/' + exerciseId,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(updatedData),
            success: function(response) {
                $('#editExerciseModal').modal('hide');
                $('#exerciseTable').DataTable().ajax.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error updating exercise:', status, error);
            }
        });
    });


// Event listener for Delete button
$('#exerciseTable').on('click', '.delete-btn', function() {
    var exerciseId = $(this).data('id');
    if (confirm('Are you sure you want to delete this exercise?')) {
        // AJAX request to delete the exercise
        $.ajax({
            url: '/fitness/exercises-and-workouts/delete-exercise/' + exerciseId,
            type: 'DELETE',
            success: function(response) {
                // Reload the DataTable to reflect changes
                $('#exerciseTable').DataTable().ajax.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error deleting exercise:', status, error);
            }
        });
    }
});
});