// define multishop namespace within window object
window.multishop = {};

// browser-wide debug log
if(window.console)
{
    window.multishop.log = window.console.log;
}
else if(window.opera)
{
    window.multishop.log = window.opera.postError;
}
else {
    window.multishop.log = function(){};
}

/* Enable stats of traffic */
var ismobile = (/iphone|ipod|android|blackberry|mini|palm|smartphone|ipad|xoom|playbook|tablet|mobile|kindle/i.test(navigator.userAgent.toLowerCase()));
if (ismobile) {
    $(document).ready(function(){
        $.ajax({
        url: '/stats/mobile/',
        cache: false,
        type: "GET",
        data: {"window_width": window.innerWidth,
        "window_height": window.innerHeight,
        "screen_width": screen.width,
        "screen_height": screen.height,
        "device_pixel_ratio": window.devicePixelRatio},
        });
    });
}

$(document).ready(function() {

    // Set timeout to close all alert messages
    setTimeout(function() {
        $(".messages").children().each(function(){
            $(this).alert('close')})},
        5000);

    // remove error warnings when fixing the error
    $(".form-group input, .form-group select, .form-group textarea").on(
        "focus", function(){
            $(this).siblings(".error-inline").hide();
        });

    // focus on the first element with error
    var errs = document.getElementsByClassName("has-error");
    if (errs.length > 0) {
        var ins = errs[0].getElementsByTagName("input");
        if (ins.length > 0) {
            ins[0].focus();
        }
    }

});
