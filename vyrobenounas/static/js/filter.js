(function (window, document, $) {
    'use strict';

    $(document).ready(function () {

        $(".menuItem, .gridWrap, #sections .menu a, #topMenu a").addClass("t200");

        //** filter scroll behav
        $(window).scroll(function () {
            //console.log(scrollPos);
            var filter = $("#filterWrap"),
                filterPos = $("#header").outerHeight(),
                filterHeight = filter.outerHeight(),
                products = $("#gridWrap"),
                scrollPos = $(window).scrollTop();

            if (scrollPos >= filterPos) {
                filter.addClass("fixed-center");
                products.css("margin-top", filterHeight + "px");
            } else {
                filter.removeClass("fixed-center");
                products.css("margin-top", "");
            }
        });


        //** filter click
        $(".filterCheck").click(function () {
            var filterPos = $("#header").outerHeight(),
                filter = $(this).attr("filter"),
                filterActive = [];

            if (filter === "all") {
                $(".filterCheck").not(this).prop("checked", false);
            } else {
                $(".filterCheck[filter=all]").prop("checked", false);
            }

            if ($(".filterCheck:checked").length == 0) {
                $(".filterCheck[filter=all]").prop("checked", true);
            }

            $(".filterCheck:checked").each(function () {
                var checkedFilter = $(this).attr("filter");
                filterActive.push(checkedFilter);
            });

            $(".grid-item").not(".gridMenu").hide();
            $.each(filterActive, function () {
                $(".grid-item[filter=" + this + "]").show();
            });
            /*$.each(filterActive, function(){
                $(".grid-item[filter!="+this+"]").not(".gridMenu").hide();
            });*/

            if ($(".filterCheck[filter=all]").prop("checked") == true) {
                $(".grid-item").show();
            }

            $(".grid").masonry("layout");
            $("body").stop().animate({scrollTop: filterPos}, '300', 'swing');
            //$("body").scrollTop(filterPos);
        });

    });
}(window, document, jQuery));