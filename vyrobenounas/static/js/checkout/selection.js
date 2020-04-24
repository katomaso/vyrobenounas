function toggle_container_by_input(input_id, container_id, hide_if_checked) {
    /* Toggle container's visibility based on checkbox with `input_id`.

    We backup input's attributes such as 'required' and 'optional' into data-
    attribute so the browser won't force checks on hidden fields.

    `hide_if_cheched` controls if we should hide/show when checked
    */
    function _toggle(event) {
        var input;
        if( $(input_id).is(":checked") === hide_if_checked ) {
            $(container_id).find('input').each(function(index, elem) {
                input = $(elem);
                input.attr("novalidate", "novalidate");
                // backup "required" into "data-necessity"
                if (input.attr("required") !== undefined) {
                    input.attr("data-necessity", "required");
                    input.removeAttr("required");
                }
                if (input.attr("optional") !== undefined) {
                    input.attr("data-necessity", "optional");
                    input.removeAttr("optional");
                }
            }); // end each
            $(container_id).hide();
        } else {
            $(container_id).find('input').each(function(index, elem) {
                input = $(elem);
                input.removeAttr("novalidate");
                // set attr which is in data-necessity (either required or optional)
                if(input.attr("data-necessity") !== undefined) {
                    input.attr(input.attr("data-necessity"), "");
                }
            }); // end each
            $(container_id).show();
        }
    }

    return _toggle
}


function validate_email(event) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var obj = $("#id_email");
    if (!re.test(obj.val())) return;

    $.post("/ajax/validate-email",  {'email': obj.val()}, function (data) {
        if (!data["valid"] || !data["exists"]) {
            $("#login_link").hide();
        }

        if (data["exists"] == true) {
            $("#login_link").show();
        }
    }, "json");
}


function login_link_clicked(event) {
    /* Send a POST request to login_url in order to pre-fill email. */
    event.stopPropagation();

    // in login form the "username" aka email is called "login"
    var form = document.getElementById("form0");
    var mail = form["email"];
    mail.setAttribute("name", "login");

    // send "next" as well to be redirected back
    var next = document.createElement("input")
    next.setAttribute("name", "next");
    next.setAttribute("type", "hidden");
    next.setAttribute("value", window.location.pathname);
    form.appendChild(next);

    // submit the form to the correct location
    var link = document.getElementById("login_link_send");
    form.setAttribute("action", link.href);

    return form.submit();
}


$(document).ready(function() {
    var toggle_billing_address = toggle_container_by_input(
            "#id_addresses_the_same", "#billing_container", true),
        toggle_address_if_necessary = toggle_container_by_input(
            "#id_necessary", "#address_container", false);

    // define hooks
    $("#id_addresses_the_same").on("change", toggle_billing_address);
    $("#id_necessary").on("change", toggle_address_if_necessary);

    $("#id_email")
        .on("blur", validate_email)
        .on("keyup", validate_email);
    $("#login_link").hide();
    $("#login_link_send").on("click", login_link_clicked);

    // launch hook functions upon loading of the document
    toggle_billing_address();
    toggle_address_if_necessary();
})