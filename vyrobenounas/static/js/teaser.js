$(document).ready(function() {

    $("#czechCarousel").carousel('cycle');

    setTimeout(function(){
        $(".messages").children().each(function(){
            $(this).alert('close')})},
        5000);
});