(function (window, document, $) {
    "use strict";

    function isVisible(selector) {
        var elementHeight = $(selector).outerHeight(),
            elementPos = $(selector).offset().top + elementHeight;
        return $(window).scrollTop() > elementPos;
    }

    function scrollTo(position) {
        $(window).scroll(position);
        $("html,body").animate({scrollTop: position}, '500', 'swing');
    }

    $(document).ready(function () {
        $(".menuItem, .gridWrap, #sections .menu a, #topMenu a").addClass("t200");

        /** recalculate grid **/
        $('.grid').masonry();
        $("img").on('load', function () {
            $('.grid').masonry("layout");
        });

        /** grid images **/
        /*$(".gridWrap").each(function(){
            var gridId = $(this).attr("gridId");
            var type = $(this).parent().attr("type");
            $(this).find(".gridImg").attr("src","images/"+type+"/" + gridId + ".jpg");
        });*/

        /** top menu - burger **/
        $("#burger").click(function () {
            $("#topMenu").fadeToggle(200);
            $(".small").toggleClass("hidden");
            $(this).toggleClass("close");
            $("body").toggleClass("fixed");
        });

        /** search small **/
        $("#search-small").click(function () {
            $("#search-input-small-wrap").fadeToggle(200);
            $("#burger, #basket-small").toggle();
        });


        /** show/hide elementy **/
        $(window).scroll(function () {
            var windowWidth = $(this).outerWidth();

            /** kosik **/
            if (windowWidth > 780) {
                if (!isVisible("#topMenu") && !isVisible("#basket")) {
                    $("#basket").addClass("fixed-right");
                    $("#basket").hide().fadeIn(300);
                } else if (isVisible("#topMenu") && $("#basket").hasClass("fixed-right")) {
                    $("#basket").removeClass("fixed-right");
                    $("#basket").hide().fadeIn(300);
                }
            }
        });

        /** scroll-button **/
        $(window).scroll(function () {
            if (!isVisible("#header")) {
                $("#scroll-button").stop().fadeIn(300);
            } else {
                $("#scroll-button").stop().fadeOut(100);
            }
        });
        $("#scroll-button").click(function () {
            scrollTo(0);
        });

        /** recalculate grid **/
        $('.grid').masonry("layout");
    });

}(window, document, jQuery));

