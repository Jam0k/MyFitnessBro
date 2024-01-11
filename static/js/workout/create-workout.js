$(document).ready(function() {
    var table = $('#exercisesTable').DataTable({
        'ajax': '/fitness/exercises-and-workouts/get-exercises',
        'columns': [
            { 'data': 'name' },
            {
                'data': 'id',
                'render': function(data, type, row) {
                    return '<input type="checkbox" class="exercise-select" value="' + row.id + '">';
                },
                'orderable': false
            }
        ]
    });

    $('#createWorkoutForm').on('submit', function(e) {
        e.preventDefault();

        var selectedExercises = [];
        $('.exercise-select:checked').each(function() {
            selectedExercises.push(this.value);
        });

        if(selectedExercises.length === 0) {
            alert('Please select at least one exercise.');
            return;
        }

        $.ajax({
            url: '/fitness/exercises-and-workouts/create-workout-plan',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'workout_name': $('#workoutName').val(),
                'selected_exercises': selectedExercises
            }),
            success: function(response) {
                window.location.href = '/fitness/exercises-and-workouts';
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error('Submission failed:', status, error);
            }
        });
    });
});
