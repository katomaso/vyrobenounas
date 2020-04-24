$(document).ready(function(){

    $(".h3-collapse").each(function(){
        var h3 = $(this);
        $(h3.attr("data-target")).on("show.bs.collapse", function() {
            h3.children("a").each(function() {
                $(this).removeClass("glyphicon-chevron-right");
                $(this).addClass("glyphicon-chevron-down");
            });
        });

        $(h3.attr("data-target")).on("hide.bs.collapse", function() {
            h3.children("a").each(function() {
                $(this).removeClass("glyphicon-chevron-down");
                $(this).addClass("glyphicon-chevron-right");
            });
        });
    });
});
