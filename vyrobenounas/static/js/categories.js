$(document).ready(function() {
    // global collapse event animation
    $(".subcategory").on("show.bs.collapse", function() {
        $(this).siblings(".collapse-right").each(function() {
            $(this).removeClass("glyphicon-chevron-right");
            $(this).addClass("glyphicon-chevron-down");
        });
    });
    $(".subcategory").on("hide.bs.collapse", function() {
        $(this).siblings(".collapse-right").each(function() {
            $(this).removeClass("glyphicon-chevron-down");
            $(this).addClass("glyphicon-chevron-right");
        });
    });
});


function unfold_category(category_id) {
    // unfold active categories in cached category list
    var active_category = $(category_id);
    var parent_element = $(active_category.parent());
    active_category.addClass("active");
    // unfold child of the current category
    if(active_category.children("ul").hasClass("collapse")) {
      active_category.children("ul").collapse("show");
    }
    // unfold all ancestors
    while( parent_element.hasClass("subcategory") ) {
      parent_element.collapse('show');
      parent_element = parent_element.parent().parent();
    }
}
