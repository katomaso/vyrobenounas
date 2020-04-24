function geocode_make_query() {
    var street = $("#id_position-street").val();
    var city = $("#id_position-city").val();
    if(!street || !city) return geocode_fail();
    var data = Array(street, city);

    var country_option = $("#id_position-country option:selected");
    if (country_option.val()) {
        data.push(country_option.text());
    }

    return data.join(", ");
}

function geocode() {
    // if(event) event.stopPropagation();
    var container = $("#id_position-city").parent();
    // if the marker was already dragged, don't update the position from address
    if($("#id_position-position").val() && multishop.map_dragged) {
        precise_position();
        return true;
    }

    if($("#id_position-position_x").val() && $("#id_position-position_y").val() && multishop.map_dragged) {
        precise_position();
        return true;
    }

    var query = geocode_make_query();
    if (!query) {
        // container.children("span").remove();
        // container.append('<span class="alert alert-error">Nevyplněná povinná pole</span>');
        return false;
    } else {
        new SMap.Geocoder(query, geocode_callback, {url:"http://api4.mapy.cz/geocode"});
        container.children("span").remove();
        container.append('<span class="help-inline">Zjišťuji adresu...</span>');
    }
    return true;
}

function geocode_callback(geocoder) {
    if (!geocoder.getResults().length || !geocoder.getResults()[0]) {
        return geocode_fail();
    }
    var item = geocoder.getResults()[0].results[0];
    if(!item) {
        return geocode_fail();
    }
    var address = item.label.split(",");
    var street = address[0].trim();
    var city = address[1].trim();
    $("#id_position-city").val(city);
    var container = $("#id_position-city").parent();
    container.children("span").remove();
    container.append('<span class="help-inline">V pořádku.</span>');
    update_position_field(item.coords);
    precise_position(item.coords);
}

function update_position_field(coords) {
    var point = coords.toWGS84();
    // multishop.log("Position updated to " + point.join(" "));
    $("#id_position-position").val("POINT("+point.join(" ")+")");
    $("#id_position-position_x").val("POINT("+point[0]+")");
    $("#id_position-position_y").val("POINT("+point[1]+")");
}

function geocode_fail() {
    $("#id_position-position").val(null);
    var container = $("#id_position-city").parent();
    container.children("span").remove();
    container.append('<span class="alert">Nepodařilo se zaměřit adresu.</span>');
    return false;
}

function coords_from_position() {
    var point = $("#id_position-position").val();
    point = point.substr("POINT(".length);
    point = point.substr(0, point.length-1);
    var arr = point.split(" ");
    if(arr.length != 2) {
        return false;
    }
    return SMap.Coords.fromWGS84(parseFloat(arr[0]), parseFloat(arr[1]));
}

function precise_position(coords) {
    $("#mapModal").delay(1000).modal('show');

    var map_div = $("#map");
    if (!map_div.hasClass("map_loaded")) {
        if(!coords) {
            var container = $("#id_position-city").parent();
            container.children("span").remove();
            container.append('<span class="alert">Nelze upřesnit adresu kvůli špatnému formátu dat.</span>');
            return false;
        }

        var map = new SMap(JAK.gel("map"), coords, 13);
        map.addDefaultLayer(SMap.DEF_BASE).enable();
        map.addDefaultControls();

        var mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM);
        map.addControl(mouse);

        map_div.addClass("map_loaded");

        var marker_layer = new SMap.Layer.Marker();
        map.addLayer(marker_layer).enable();

        var mark = new SMap.Marker(coords);
        mark.decorate(SMap.Marker.Feature.Draggable);
        marker_layer.addMarker(mark);

        map.marker_layer = marker_layer;

        var signals = map.getSignals();

        signals.addListener(window, "marker-drag-stop", function (e) {
            var node = e.target.getContainer();
            node[SMap.LAYER_MARKER].style.cursor = "";
            var coords = e.target.getCoords();
            update_position_field(coords);
            multishop.marker_dragged = true;
        });

        signals.addListener(window, "marker-drag-start", function (e) {
            var node = e.target.getContainer();
            node[SMap.LAYER_MARKER].style.cursor = "pointer";
        });

        window.multishop.map = map;
    } else {
        if(!multishop.marker_dragged) {
            // var marker_layer = multishop.map._layers.filter(function (e, i, a) {return ("_markers" in e)})[0];
            var marker = multishop.map.marker_layer.getMarkers()[0];
            marker.setCoords(coords);
            multishop.map.marker_layer.positionMarker(marker);
            multishop.map.marker_layer.redraw(true);
        }
    }
    setTimeout('multishop.map.syncPort()', 200);
}

function delayed_geolocation() {
    multishop.marker_dragged=false;
    $(document).clearQueue("events");
    $(document).queue("events", Array()).delay(3000, "events").queue("events", geocode).dequeue("events");
}

function position_toggle(e) {
    if ($("#id_position-address_visible").is(":checked")) {
        $('#position_fields').show();
    } else {
        $('#position_fields').hide();
    }
}


$(document).ready(function() {
    // hide and show position fields based on status of the checkbox
    $("#id_position-address_visible").on("change", position_toggle);
    position_toggle(null);

    // signals which makes map to update based on values from form
    $("#id_position-country").on("change", function(event){multishop.marker_dragged=false;});

    $("#id_position-street").on("keydown", delayed_geolocation);
    $("#id_position-street").on("change", delayed_geolocation);
    $("#id_position-city").on("keydown", delayed_geolocation);
    $("#id_position-city").on("change", delayed_geolocation);

    if (!$("#id_position-address_visible").is(":checked")) {
            return true;
        }

    $("#shop-form").on("submit", function(event){
        // don't launch locator when the address is not visible
        if (!$("#id_position-address_visible").is(":checked")) {
            return true;
        }

        if (!$("#id_position-position").val()) {
            // locate a shop if not yet located
            if(!geocode(event)) {
                $("#shop-form input[type='submit']").each(function() {
                    $(this).popover({
                        title: "Chyba ve formuláři",
                        content: "Nelze stanovit adresu Vašeho kamenného obchodu",
                        trigger: "manual",
                        placement: "top"
                    });
                    $(this).popover("show");
                    setTimeout("$(\"#shop-form input[type='submit']\").popover(\"destroy\")", 2000);
                });
            }
            return false;
        }
        return true;
    });
});
