(function ($) {
    'use strict';

    $(function () {
        $('.half').hover(function () {
            $(this).find('.topPage').stop().fadeOut(200);
        }, function () {
            $(this).find('.topPage').stop().fadeIn(100);
        });
    });
}(jQuery));