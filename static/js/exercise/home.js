document.addEventListener("DOMContentLoaded", function () {
  const dateInput = document.getElementById("dateFilter");

  // Initialize the DataTables
  const exerciseLogsTable = $("#exercise-logs-table").DataTable({
    columns: [
      { data: "name" },
      { data: "sets" },
      { data: "reps" },
      { data: "weight" },
      { data: "notes" },
      {
        data: "id", // Assuming 'id' is the identifier for exercise logs
        render: function (data, type, row) {
          return (
            '<button class="btn btn-danger delete-exercise-btn" data-id="' +
            data +
            '">Delete</button>'
          );
        },
        orderable: false,
      },
    ],
  });

  const cardioLogsTable = $("#cardio-logs-table").DataTable({
    columns: [
        { data: "activity" },
        { data: "duration" },
        { data: "calories_burned" },
        { data: "notes" },
        {
            data: "id",
            render: function (data, type, row) {
                return '<button class="btn btn-danger delete-cardio-btn" data-id="' + data + '">Delete</button>';
            },
            orderable: false
        }
    ],
});

  // Function to fetch logs
  function fetchLogs(date) {
    fetch("/fitness/tracking", {
      method: "POST",
      body: new URLSearchParams({ date: date }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const exerciseLogs = data.exercise_logs;
        const cardioLogs = data.cardio_logs;

        // Clear and populate the exercise logs table
        exerciseLogsTable.clear();
        if (exerciseLogs.length > 0) {
          exerciseLogs.forEach((log) => {
            exerciseLogsTable.row.add({
              name: log.name,
              sets: log.sets,
              reps: log.reps,
              weight: log.weight,
              notes: log.notes,
              id: log.id,
            });
          });
        }
        exerciseLogsTable.draw();

        // Clear and populate the cardio logs table
        cardioLogsTable.clear();
        if (cardioLogs.length > 0) {
          cardioLogs.forEach((log) => {
            cardioLogsTable.row.add({
              activity: log.activity,
              duration: log.duration,
              calories_burned: log.calories_burned,
              notes: log.notes,
              id: log.id,
            });
          });
        }
        cardioLogsTable.draw();
      });
  }

  // Event listener for date input
  dateInput.addEventListener("input", function () {
    const selectedDate = dateInput.value;
    fetchLogs(selectedDate);
  });

  // Set current date and fetch logs
  const current_date = new Date().toISOString().split("T")[0]; // Get current date in YYYY-MM-DD format
  dateInput.value = current_date;
  fetchLogs(current_date);

  // Event listener for delete exercise log
  $('#exercise-logs-table').on('click', '.delete-exercise-btn', function() {
    const logId = $(this).data('id');
    if (confirm('Are you sure you want to delete this exercise log?')) {
        $.ajax({
            url: 'delete-exercise-log/' + logId,
            type: 'DELETE',
            success: function(response) {
                fetchLogs($('#dateFilter').val()); // Manually fetch logs to refresh data
            },
            error: function(xhr, status, error) {
                console.error('Error deleting exercise log:', status, error);
            }
        });
    }
});


    // Event listener for delete cardio log
    $('#cardio-logs-table').on('click', '.delete-cardio-btn', function() {
      const logId = $(this).data('id');
      if (confirm('Are you sure you want to delete this cardio log?')) {
          $.ajax({
              url: 'delete-cardio-log/' + logId,
              type: 'DELETE',
              success: function(response) {
                  fetchLogs($('#dateFilter').val()); // Manually fetch logs to refresh data
              },
              error: function(xhr, status, error) {
                  console.error('Error deleting cardio log:', status, error);
              }
          });
      }
  });
});
