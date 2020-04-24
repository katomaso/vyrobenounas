function shipping_toggle(e) {
    if ($("#id_addresses_the_same").is(":checked")) {
        $('#shipping-address').hide();
        $('#billing-address').removeClass("col-md-6");
    } else {
        $('#shipping-address').show();
        $('#billing-address').addClass("col-md-6");
    }
}

$(document).ready(function() {
    $("#id_addresses_the_same").on("change", shipping_toggle);
    shipping_toggle(null);
})