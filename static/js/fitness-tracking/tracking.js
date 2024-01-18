document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("dateFilter");
    const exerciseLogsTable = $("#exercise-logs-table").DataTable({
      columns: [
        { data: "name" },
        { data: "sets" },
        { data: "reps" },
        { data: "weight" },
        { data: "notes" },
      ],
    });

    const workoutPlanLogsTable = $("#workout-plan-logs-table").DataTable({
        columns: [
            { data: "workout_plan.name" },
            {
                data: "workout_plan.id", // Access the ID here
                render: function (data, type, row) {
                    return (
                        '<button class="btn btn-success view-exercises-btn" data-id="' +
                        data +
                        '">View Exercises</button>'
                    );
                },
                orderable: false,
            },
        ],
    });

    const cardioLogsTable = $("#cardio-logs-table").DataTable({
        columns: [
            { data: "cardio_log.name" },
            { data: "cardio_log.activity" },
            { data: "cardio_log.duration" },
            { data: "cardio_log.calories_burned" },
            { data: "cardio_log.notes" },
        ],
    });

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
    
          exerciseLogsTable.clear().draw();
          cardioLogsTable.clear().draw();
    
          if (exerciseLogs.length > 0) {
            exerciseLogsTable.rows.add(exerciseLogs).draw();
          }
    
          if (cardioLogs.length > 0) {
            cardioLogsTable.rows.add(cardioLogs).draw();
          }
        });
      }
    
      dateInput.addEventListener("input", function () {
        const selectedDate = dateInput.value;
        fetchLogs(selectedDate);
      });
    
      const current_date = new Date().toISOString().split('T')[0]; // Get current date in YYYY-MM-DD format
      dateInput.value = current_date;
      fetchLogs(current_date);
    });



