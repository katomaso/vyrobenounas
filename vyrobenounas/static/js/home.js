/* jslint white:on */
(function (document, $) {
  "use strict";

  $(document).on('ready', function () {
    var $carousel = $('.main-carousel').flickity({
        pageDots: false,
        prevNextButtons: false,
        draggable: false,
        selectedAttraction: 0.09,
        friction: 0.5
      }),
      $flkty = $carousel.data('flickity'),
      $cellButtons = $("#productsMenuIn").find('.slideMenuButton');

    // update selected cellButtons
    $carousel.on('select.flickity', function() {
      $cellButtons.filter('.is-selected')
      .removeClass('is-selected');
    $cellButtons.eq( flkty.selectedIndex ).addClass('is-selected');
    });

    /** redirect to product - test **/
    /*$("#gridWrap.main .gridWrap").not("#productsMenuWrap").click(function(){
      window.location.href = "product.php";
    });*/

    /** submenu button click **/
    $(document).on("click", ".menuItem.parent", function(){
      var menuLink = $(this).attr("menuLink");
      var menuText = $(this).text();
      var menuLevelClicked = flkty.selectedIndex;
      var menuLevelCurrent = menuLevelClicked + 1;
      console.log("clicked at: "+menuLevelClicked);
      console.log("current menu: "+menuLevelCurrent);
      var prevMenuHeader = $("#menuHeader").text();
      console.log("prevMenuHeader: "+prevMenuHeader);
      $("#productsMenuIn").find('#prevButton').fadeIn(200);

      // nacteni submenu
      $.ajax({
        url: "menu/"+menuLink+".html",
        success: function(data) {
          var $cellElems = $(""+data+"");
          //var object = $(".carousel-cell[menuLevel='"+menuLevelCurrent+"']");
          //$carousel.flickity('remove', object);
          $carousel.flickity('insert', $cellElems, menuLevelCurrent);
          $carousel.flickity('select', menuLevelCurrent );
          changeMenuHeader();
          addPrevButton();
          menuRefresh();
          gridRefresh();
        },
        complete: function(){
          //console.log("complete");
        },
        error: function() {
          console.log("chyba načtení menu");
        }
      });
    });

    /** menu prevmenu click **/
    $(document).on("click", ".prevButton", function() {
      var menuLevelClicked = flkty.selectedIndex;
      console.log("clicked at: "+menuLevelClicked);
      //var object = $(".carousel-cell[menu-level='"+menuLevelClicked+"']");
      var object = $(".carousel-cell").eq(menuLevelClicked);
      $carousel.flickity('previous');
      $carousel.on('settle.flickity', function() {
      // při dokončení animace slidu
        $carousel.flickity('remove', object);
        menuRefresh();
        gridRefresh();
      });
      var menuLevelCurrent = flkty.selectedIndex;
      console.log( 'carousel at ' + menuLevelCurrent );
      if (menuLevelCurrent == 0) {
        console.log("clicked: "+menuLevelClicked);
        $(this).fadeOut(100);
      }
      changeMenuHeader();
      addPrevButton();
    });

    function changeMenuHeader() {
      var currentMenuLevel = flkty.selectedIndex;
      //console.log("currentLevel:"+currentMenuLevel);
      var menuHeader = $(".menuCell").eq(currentMenuLevel).attr("menu-title");
      //console.log(menuHeader);
      $("#menuHeader").text(menuHeader);
    }

    function addPrevButton() {
      var menuLevelCurrent = flkty.selectedIndex;
      var prevMenuHeader = $(".carousel-cell").eq(menuLevelCurrent-1).attr("menu-title");
      var prevButton = $(".carousel-cell").eq(menuLevelCurrent).find(".prevButton").length;
      if (prevButton == 0) {
        var prevButtonHtml = "<li class='menuItem prevButton t200'><div class='prevMenu' class='slideMenuButton'><i class='fa fa-caret-left' aria-hidden='true'></i></div>Zpět na " + prevMenuHeader + "</li>";
        $(".carousel-cell").eq(menuLevelCurrent).find(".subMenu").append(prevButtonHtml);
      }
    }

    function menuRefresh() {
      $carousel.flickity('reloadCells');
    }

    function gridRefresh() {
      console.log("grid refresh");
      $('.grid').masonry("layout");
    }
  });
})(document, jQuery);