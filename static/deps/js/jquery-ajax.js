// When the HTML document is ready (rendered)
$(document).ready(function () {
    // Element with id jq-notification, used for notifications from ajax
    var successMessage = $("#jq-notification");

    // Element with id notification, used for notifications from django
    var notification = $('#notification');
    // Hide it after 7 seconds
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // Open the cart modal when the cart icon is clicked
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Click on the close button of the cart modal
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Handler for the delivery method radio buttons
    $("input[name='requires_delivery']").change(function() {
        var selectedValue = $(this).val();
        // Show or hide the delivery address input
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });


    // Click on the add to cart button
    $(document).on("click", ".add-to-cart", function (e) {
        // Prevent the default action
        e.preventDefault();

        // Take the counter element in the cart icon and read its value
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get the product id from the data-product-id attribute
        var product_id = $(this).data("product-id");

        // Take the django view URL from the href attribute
        var add_to_cart_url = $(this).attr("href");

        // Send a POST request via ajax without reloading the page
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Message
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Hide the message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Increase the number of items in the cart (rendered in the template)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Replace the cart content with the django response (newly rendered cart markup)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error while updating the cart");
            },
        });
    });




    // Click on the remove from cart button
    $(document).on("click", ".remove-from-cart", function (e) {
        // Prevent the default action
        e.preventDefault();

        // Take the counter element in the cart icon and read its value
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get the cart id from the data-cart-id attribute
        var cart_id = $(this).data("cart-id");
        // Take the django view URL from the href attribute
        var remove_from_cart = $(this).attr("href");

        // Send a POST request via ajax without reloading the page
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Message
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Hide the message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Decrease the number of items in the cart (rendering)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Replace the cart content with the django response (newly rendered cart markup)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error while updating the cart");
            },
        });
    });




    // Now the + and - quantity buttons 
    // Handler for decreasing the value
    $(document).on("click", ".decrement", function () {
        // Take the django view URL from the data-cart-change-url attribute
        var url = $(this).data("cart-change-url");
        // Take the cart id from the data-cart-id attribute
        var cartID = $(this).data("cart-id");
        // Find the nearest quantity input 
        var $input = $(this).closest('.input-group').find('.number');
        // Read the product quantity
        var currentValue = parseInt($input.val());
        // Decrease by 1 only if the quantity is greater than one
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Call the function defined below
            // with arguments (cart id, new quantity, whether the quantity went down or up, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Handler for increasing the value
    $(document).on("click", ".increment", function () {
        // Take the django view URL from the data-cart-change-url attribute
        var url = $(this).data("cart-change-url");
        // Take the cart id from the data-cart-id attribute
        var cartID = $(this).data("cart-id");
        // Find the nearest quantity input 
        var $input = $(this).closest('.input-group').find('.number');
        // Read the product quantity
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Call the function defined below
        // with arguments (cart id, new quantity, whether the quantity went down or up, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
 
            success: function (data) {
                // Message
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Hide the message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Update the number of items in the cart
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Replace the cart content
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Error while updating the cart");
            },
        });
    }

    // Format the phone number input as (xxx) xxx-xxxx
    var phoneInput = document.getElementById('id_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    }

    // Client-side check that the phone number has the right format
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            // Strip brackets and dashes from the phone number before submitting the form
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });
});