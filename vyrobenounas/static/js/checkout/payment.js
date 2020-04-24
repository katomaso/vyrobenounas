$(document).ready(function() {
    $("#id_payment input").on("change", function() {
        if ($("#id_payment_0").is(":checked")) {
            $("#submit").val("Objednat");
        } else {
            $("#submit").val("Zaplatit");
        }
    })
})