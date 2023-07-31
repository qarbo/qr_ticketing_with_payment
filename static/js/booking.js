$(document).ready(function() {
    var field1 = $("#field1");
    var field2 = $("#field2");

    // Function to toggle the visibility of the form fields
    function toggleFields() {
        field1.toggle();
        field2.toggle();
    }

    // Bind the toggleFields function to the click event of the toggle button
    $("#toggle-button").on("click", toggleFields);
});