
$(document).ready(function(){
    // URL needs to be in HTML bcs it gets rendered - URL is python-dependent
    var admin_ajax_url = $("#why_hint_a").attr("data-url");

    function product_name_selected(event, term, autocomplete) {
        $.get(
            admin_ajax_url,
            {action: "render_product_box", 'id': term.attr("data-value")},
            function(data, status, xhr) {
                if( data.status != "success") {
                    return alert(data.message);
                }
                $("#add_title").attr("data-original", $("#add_title").text()).text("Přidat nabídku");
                $("#product_part").hide()
                $("#product_box").attr("data-loaded", "true").html(data.html);
                $("#submit_buttons").insertAfter(".field-shipping_price");
                $("#id_product").val(data.pk);
            }, "json"
        );
    }

    function product_name_not_selected(event) {
        var value = $(this).val()
        if ($("#product_box").attr("data-loaded") == "true") {
            $("#product_box").attr("data-loaded", "false").empty();
            $("#id_product").val("");
            $("#add_title").text($("#add_title").attr("data-original"));
        }
        else  // if product NOT loaded
        {
            $("#new_product_title").html("Popište \"" + value + "\"");
        }

        if ($("#product_part").is(":hidden") && value.length >= 3) {
            $("#product_part").show();
        }

        if (!$("#product_part").is(":hidden") && value.length <= 2) {
            $("#product_part").hide();
        }

    }


    $("#id_name").on('selectChoice', product_name_selected);
    $("#id_name").on('keyup.autocomplete', product_name_not_selected);

    $("#why_hint_a").popover();

});