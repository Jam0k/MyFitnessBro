$(document).ready(function() {
    // DataTable initialization
    var exerciseTable = $('#exerciseTable').DataTable({
    ajax: '/fitness/exercises-and-workouts/get-exercises', // Adjust the URL
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
        data: 'id',
        render: function(data, type, row) {
          return '<input type="checkbox" class="exercise-select" value="' + data + '">';
        },
        orderable: false
      }
    ]
  });
  
  
    // Form submission handling
    $('#logExerciseForm').submit(function(e) {
      e.preventDefault();
  
      // Get selected exercise IDs
      var selectedExerciseIds = $('.exercise-select:checked').map(function() {
        return $(this).val();
      }).get();
  
      // Get the selected date
      var logDate = $('#exerciseDate').val();
  
      // Prepare the data to be submitted
      var logData = {
        date: logDate,
        exercise_ids: selectedExerciseIds
      };
  
      // Submit the log data to your Flask route
      $.ajax({
        url: '/fitness/exercises-and-workouts/log-exercise',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(logData),
        success: function(response) {
          // Handle success, e.g., show a success message
          alert('Exercise(s) logged successfully');
        },
        error: function(xhr, status, error) {
          // Handle errors, e.g., display an error message
          alert('Error logging exercise(s): ' + status);
        }
      });
    });
  });