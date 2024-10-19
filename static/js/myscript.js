$(document).ready(function () {
    // Function to update the total amount
    function updateTotalAmount() {
        let total = 0;
        $('.cart-item').each(function () {
            const price = parseFloat($(this).data('price'));
            const quantity = parseInt($(this).find('.quantity-value').text());
            const itemTotalPrice = price * quantity;
            $(this).find('.item-total-price').text(itemTotalPrice.toFixed(2));
            total += itemTotalPrice;
        });
        $('#totalamount').text(total.toFixed(2));
    }

    // Handle the plus button click
    $('.plus-cart').click(function (e) {
        e.preventDefault();
        const pid = $(this).attr('pid');
        const quantityElement = $(this).siblings('.quantity-value');
        let quantity = parseInt(quantityElement.text()) + 1;

        // AJAX request to update the cart quantity
        $.ajax({
            url: '/update_cart_quantity',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ cart_item_id: pid, quantity: quantity }),
            success: function (response) {
                quantityElement.text(response.quantity);
                updateTotalAmount();
            },
            error: function (error) {
                console.log('Error updating cart:', error);
            }
        });
    });

    // Handle the minus button click
    $('.minus-cart').click(function (e) {
        e.preventDefault();
        const pid = $(this).attr('pid');
        const quantityElement = $(this).siblings('.quantity-value');
        let quantity = parseInt(quantityElement.text()) - 1;

        // Ensure quantity doesn't go below 1
        if (quantity < 1) return;

        // AJAX request to update the cart quantity
        $.ajax({
            url: '/update_cart_quantity',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ cart_item_id: pid, quantity: quantity }),
            success: function (response) {
                quantityElement.text(response.quantity);
                updateTotalAmount();
            },
            error: function (error) {
                console.log('Error updating cart:', error);
            }
        });
    });
    $('.remove-cart').click(function (e) {
        e.preventDefault();
        const pid = $(this).attr('pid');

        // AJAX request to remove the cart item
        $.ajax({
            url: '/remove_cart_item',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ cart_item_id: pid }),
            success: function (response) {
                // On success, remove the cart item from the DOM
                $(`.cart-item[data-cart-item-id='${pid}']`).remove();
                updateTotalAmount(); // Update total amount after removing item
            },
            error: function (error) {
                console.log('Error removing cart item:', error);
            }
        });
    });
});