$(function(){
	var popup = $("#popup");
	var window = $("#popup .window");
	
	//** popup click - show
	$("[popup]").click(function(){
		var contentName = $(this).attr("popup");
		//var pageH = $(window).outerHeight();
		
		var bodyH = $("body").outerHeight();
		
		var page = $.get("pages/"+contentName+".html", function(){
			console.log("nahráno");
			//console.log(page.responseText);
			$("#popup .content").html(page.responseText);
			/*popup.show();
			popup.hide();*/
			
			popup.fadeIn(300).addClass(contentName);			
			var pageW = $(document).outerWidth();
			var windowW = window.outerWidth();
			console.log("pageW: "+pageW);
			console.log("windowW: "+windowW);
			window.css({
				"left": (pageW / 2) - (windowW / 2) + "px",
				"max-width": (pageW * 0.8) + "px"
			});
			$("body").addClass("fixed");
		});		
	});
	
	//** popup close
	$("#popup .close").click(function() {
		$("#popup").fadeOut(100);
		$("body").removeClass("fixed");
	});
	
});