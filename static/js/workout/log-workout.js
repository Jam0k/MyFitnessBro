$(document).ready(function() {
    // Initialize an array to store selected workout IDs
    let selectedWorkoutIds = [];
  
    // DataTable initialization for workout plans
    $('#workoutTable').DataTable({
      responsive: true,
      ajax: '/fitness/exercises-and-workouts/get-workout-plans',
      columns: [
        { data: 'name' },
        {
          data: 'id',
          render: function(data, type, row) {
            return '<button type="button" class="btn btn-primary workout-select" value="' + data + '">Select</button>';
          },
          orderable: false
        }
      ]
    });
  
    // Event handler for workout selection button
    $('#workoutTable').on('click', '.workout-select', function() {
      var workoutId = $(this).val();
      if ($(this).hasClass('btn-success')) {
        // Deselect the workout and remove from array
        $(this).removeClass('btn-success').addClass('btn-primary');
        selectedWorkoutIds = selectedWorkoutIds.filter(id => id !== workoutId);
      } else {
        // Select the workout and add to array
        $(this).addClass('btn-success').removeClass('btn-primary');
        selectedWorkoutIds.push(workoutId);
      }
    });
  
    // Form submission handling
    $('#logWorkoutForm').submit(function(e) {
      e.preventDefault();
  
      var logDate = $('#workoutDate').val();
  
      if (!logDate || selectedWorkoutIds.length === 0) {
        alert('Please select at least one workout and choose a date.');
        return;
      }
  
      var logData = {
        date: logDate,
        workout_plan_ids: selectedWorkoutIds
      };
  
      // Submit the log data to your Flask route
      $.ajax({
        url: '/fitness/exercises-and-workouts/log-workout',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(logData),
        success: function(response) {
          alert('Workout(s) logged successfully');
        },
        error: function(xhr, status, error) {
          alert('Error logging workout(s): ' + status);
        }
      });
    });
  });