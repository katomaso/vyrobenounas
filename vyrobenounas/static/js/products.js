$(function(){	
	$('#otherProductsSlider').flickity({
		contain: true,
		//draggable: false,
		freeScroll: true,
		groupCells: true
	});
	
	var highestCell = 0;
	$("#otherProductsSlider .carousel-cell").each(function(){
		cellHeight = $(this).outerHeight();
		if (cellHeight > highestCell) {
			highestCell = cellHeight;
		}
	});
	$("#otherProductsSlider .flickity-viewport").css("height", highestCell);
	
	$('#productGallerySlider').flickity({
		contain: true,
		//draggable: false,
		freeScroll: true,
		groupCells: true
	});
	
	/** product image gallery **/
	
	/*$("#productImage .main-image").css("max-height", windowHeight/2 + "px");
	$(window).on("resize orientationchange", function(){
		$("#productImage .main-image").css("max-height", windowHeight/2 + "px");
	});
	$(".productGalleryImage").on("click tap", function(){
		var src = $(this).attr("src");
		$(".main-image").attr("src", src);
	});*/
	
	//$("#productImage .main-image").css("max-height", windowHeight/2 + "px");
	
	/** klik na kosik - test **/
	$(".addBasket").click(function(){
		var basketNumber = parseInt($("#basket .basketNumber").text()) + 1;
		$(".basketNumber").text(basketNumber);
		$(".basketNumber").fadeIn(200);
	});	
	
	/** recalculate grid **/
	$('.grid').masonry("layout");		
});