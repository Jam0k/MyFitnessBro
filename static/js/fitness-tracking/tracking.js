document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("dateFilter");
    const exerciseLogsTable = $("#exercise-logs-table").DataTable({
        columns: [
            { data: "exercise.name" },
            { data: "exercise.category" },
            { data: "exercise.duration_minutes" },
            { data: "exercise.calories_burned" },
            { data: "exercise.reps" },
            { data: "exercise.sets" },
            { data: "exercise.weight_lifted" },
            { data: "exercise.notes" },
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
                const workoutPlanLogs = data.workout_plan_logs;
                const cardioLogs = data.cardio_logs;

                exerciseLogsTable.clear().draw();
                workoutPlanLogsTable.clear().draw();
                cardioLogsTable.clear().draw();

                if (exerciseLogs.length > 0) {
                    exerciseLogsTable.rows.add(exerciseLogs).draw();
                }

                if (workoutPlanLogs.length > 0) {
                    workoutPlanLogsTable.rows.add(workoutPlanLogs).draw();
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

    $("#workout-plan-logs-table").on(
        "click",
        ".view-exercises-btn",
        function () {
            const workoutPlanId = $(this).data("id");
            viewExercises(workoutPlanId);
        }
    );

    function viewExercises(workoutPlanId) {
        $.ajax({
            url:
                "/fitness/exercises-and-workouts/get-workout-plan/" + workoutPlanId,
            type: "GET",
            success: function (response) {
                const exercises = response.exercises;

                // Destroy existing DataTable if it exists
                if ($.fn.DataTable.isDataTable("#exercisesDataTable")) {
                    $("#exercisesDataTable").DataTable().destroy();
                }

                // Create DataTable
                $("#exercisesDataTable").DataTable({
                    responsive: true,
                    data: exercises,
                    columns: [
                        { data: "name" },
                        { data: "category" },
                        { data: "duration_minutes" },
                        { data: "calories_burned" },
                        { data: "reps" },
                        { data: "sets" },
                        { data: "weight_lifted" },
                        { data: "notes" },
                    ],
                    searching: false, // Disable searching if not needed
                    paging: false, // Disable pagination if not needed
                    info: false, // Disable info text if not needed
                });

                $("#viewExercisesModal").modal("show");
            },
            error: function (xhr, status, error) {
                console.error("Error fetching exercises:", status, error);
            },
        });
    }

});





