$(document).ready(function () {
    // Loop through each table with an ID that starts with 'mealTypeTable'
    $("table[id^='mealTypeTable']").each(function () {
        // Initialize DataTables on each table
        $(this).DataTable();
    });
});
