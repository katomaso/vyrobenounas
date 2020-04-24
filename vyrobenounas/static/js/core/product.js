
function toggle_price(formid) {
	var form = $("#" + formid);

	$(".hide-on-success").each(function() {
		var other_form = $(this);
		if (other_form.attr("id") == formid) return;
		other_form.hide();
		other_form.siblings(".price").show();
	});

	form.toggle();
	form.siblings(".price").toggle();
}

/* Handle AJAX request sending a product to the cart */
$(document).ready(function () {
	$(".add-to-cart").on("click", function (event) {
		event.preventDefault();
		event.stopPropagation();

		var button = $(this),
			form = button.parents("form").first();

		button.attr("disabled", "disabled");

		$.ajax({
			url: form.attr("action"),
			data: form.serialize(),
			method: form.attr("method").toUpperCase(),
		}).done(function (data, status, xhr) {
			var cart = $("#cart");
			button.removeClass("btn-info");
			button.addClass("btn-success");
			button.text("Přidáno");
			cart.load(cart.attr("data-reload"));
			setTimeout(function() {
				// on-success
				if(form.parent().hasClass("hide-on-success")) {
					form.parent().toggle();
					form.parent().siblings(".price").toggle();
				}
				button.removeAttr("disabled");
				button.removeClass("btn-success");
				button.addClass("btn-info");
				button.text(button.attr("data-text"));
			}, 2000);
		 }).fail(function(xhr, status, error) {
			// on-fail
			button.text("Něco je špatně");
			button.removeClass("btn-info");
			button.addClass("btn-error");
			setTimeout(function() {
				button.removeAttr("disabled");
				button.text(button.attr("data-text"));
				button.removeClass("btn-error");
				button.addClass("btn-info");
			}, 2000);
		});
	});
});

$(document).ready(function() {
	$(".hide-on-success").children().on("click", function(e) {
		e.preventDefault();
		e.stopPropagation();
	})
})