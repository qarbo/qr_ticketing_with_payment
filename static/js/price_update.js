$(document).ready(function() {
    // Store the initial values to compare later
    var previousInputValue = "";
    var previousSelectValue = "";

    // Function to send the POST request to the backend
    function sendPostRequest(inputData, selectData) {
        $.ajax({
            type: "POST",
            url: "your_backend_url", // Replace with the actual backend URL
            data: { inputData: inputData, selectData: selectData },
            success: function(response) {
                // Update the div element with the response value
                $("#responseDiv").text(response);
            },
            error: function(xhr, status, error) {
                console.error("Error occurred:", error);
            }
        });
    }

    // Function to check for value changes in the input field and select element
    function checkInputChange() {
        var currentInputValue = $("#inputData").val();
        var currentSelectValue = $("#selectData").val();

        if (currentInputValue !== previousInputValue || currentSelectValue !== previousSelectValue) {
            previousInputValue = currentInputValue;
            previousSelectValue = currentSelectValue;
            sendPostRequest(currentInputValue, currentSelectValue);
        }
    }

    // Bind the checkInputChange function to the input field's 'input' event
    $("#inputData, #selectData").on("input change", checkInputChange);
});