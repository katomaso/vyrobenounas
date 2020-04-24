
function order_ajax_fail(button, message) {
  /*
  Mark ajax operation as failed with a message
  */
  button.prop("disabled", false);
  button.addClass("btn-danger");
  if(button.attr("data-toggle") !== undefined) {
    button.tooltip("hide").tooltip("destroy");
  }
  button.tooltip({
    placement: "top",
    trigger: "manual hover",
    title: message
  }).tooltip("show");
  return;
}

$(document).ready(function(){

  $(".submit_on_change").on("change", function() {
    if($(this).val()) {
      $(this).parent("form").submit();
    }
  })

})