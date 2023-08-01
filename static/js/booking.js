
function updatePrice(priceDiv, type, regularSelectValue, tableSelectValue) {
    let value;
    if (type === "table") {
        value = tableSelectValue;
    } else {
        value = regularSelectValue;
    }
    $.ajax({
        url: '/booking/get-price/', // Replace with the actual backend URL to handle the update
        type: 'POST',
        data: {
            type: type,
            value: value
        },
        success: function(response) {
            // Update the price element with the response from the server
            priceDiv.html('Final price / Итоговая цена: <strong>' + response['price'] + '$</strong>')
            console.log(response)
        },
        error: function() {
            priceDiv.text('Error while price getting / Ошибка при преподсчете цены')
        }
    });
}

$(document).ready(function() {

    let typeSelect = $("#id_selected_option");
    let tableSelect = $('.tables-select');
    let regularInput = $('.regular-select');
    let finalPriceText = $('.final-price');
    let tableSelectParent = tableSelect.closest('p');
    let regularInputParent = regularInput.closest('p');
    updatePrice(finalPriceText, typeSelect.val(), regularInput.val(), tableSelect.val());

    function updateSelectedOption() {
        let selectedOption = typeSelect.val();
        if (selectedOption === "table") {
            regularInputParent.hide();
            tableSelectParent.show();
        } else {
            regularInputParent.show();
            tableSelectParent.hide();
        }
        $(".hidden").hide(); // Hide all elements with class "hidden"
        $("#" + selectedOption + "_div").show(); // Show the selected option's element
        updatePrice(finalPriceText, typeSelect.val(), regularInput.val(), tableSelect.val());
    }

    tableSelectParent.hide();

    // Function to show/hide elements based on the selected option
    updateSelectedOption();
    typeSelect.change(function() {
        updateSelectedOption()
    });

    // On page load, trigger the change event to set initial visibility
    $("#my_field").trigger("change");

    tableSelect.change(function() {
        updatePrice(finalPriceText, typeSelect.val(), regularInput.val(), tableSelect.val());
    });

    regularInputParent.on('input', function() {
        updatePrice(finalPriceText, typeSelect.val(), regularInput.val(), tableSelect.val());
    });

});