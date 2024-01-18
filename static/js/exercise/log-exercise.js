$(document).ready(function() {
  // Populate exercise dropdown
  $.ajax({
    url: '/fitness/get-exercises',
    type: 'GET',
    success: function(response) {
      var exercises = response.data;
      var exerciseDropdown = $('#exerciseDropdown');
      $.each(exercises, function(index, exercise) {
        exerciseDropdown.append($('<option>', {
          value: exercise.id,
          text: exercise.name
        }));
      });
    }
  });

  // Handle form submission
  $('#logExerciseForm').submit(function(e) {
    e.preventDefault();

    var selectedExerciseId = $('#exerciseDropdown').val();
    var sets = $('#setsInput').val();
    var reps = $('#repsInput').val();
    var weight = $('#weightInput').val();
    var notes = $('#notesInput').val();
    var logDate = $('#exerciseDate').val();

    var logData = {
      exercise_id: selectedExerciseId,
      sets: sets,
      reps: reps,
      weight: weight,
      notes: notes,
      date: logDate
    };

    $.ajax({
      url: '/fitness/log-exercise',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(logData),
      success: function(response) {
        alert('Exercise logged successfully');
        // Optionally, clear the form or redirect the user
      },
      error: function(xhr, status, error) {
        alert('Error logging exercise: ' + status);
      }
    });
  });
});
