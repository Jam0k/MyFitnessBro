    // Show the alert and close the modal after 2 seconds
    function showModalAlert(message, alertType = "success") {
        const modalAlert = document.getElementById("modalAlert");
        modalAlert.innerHTML = message;
        modalAlert.className = `alert alert-${alertType}`;
        modalAlert.style.display = "block";

        // Hide the alert and close the modal after 2 seconds (2000 milliseconds)
        setTimeout(function () {
            modalAlert.style.display = "none";
            $('#createFoodModal').modal('hide');
        }, 2000);
    }

    // Submit the form asynchronously
    document.getElementById("foodForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);

        // Use AJAX to submit the form data
        $.ajax({
            type: "POST",
            url: "/nutrition/create-new-food-item",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                // Display the alert
                showModalAlert("Food item added successfully!", "success");

                // Clear the form fields if needed
                // document.getElementById("foodForm").reset();
            },
            error: function (error) {
                showModalAlert("An error occurred: " + error.responseText, "danger");
            }
        });
    });