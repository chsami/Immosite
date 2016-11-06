/**
 * Created by Sami on 17/05/2016.
 */

$( document ).ready(function() {

    function ZoomIn() {
        var current= parseInt( map.getZoom(),10);
        current++;
        if(current>20){
            current=20;
        }
        map.setZoom(current);
    }

    function ZoomOut() {
        var current= parseInt( map.getZoom(),10);
        current--;
        if(current<0){
            current=0;
        }
        map.setZoom(current);
    }


    function toggleStreetView() {
        var toggle = panorama.getVisible();
        if (toggle == false) {
            panorama.setVisible(true);
        } else {
            panorama.setVisible(false);
        }
    }

    //Check to see if the window is top if not then display button
	$(window).scroll(function(){
		if ($(this).scrollTop() > 100) {
			$('.scrollToTop').fadeIn();
		} else {
			$('.scrollToTop').fadeOut();
		}
	});

	//Click event to scroll to top
	$('.scrollToTop').click(function(){
		$('html, body').animate({scrollTop : 0},800);
		return false;
	});

    /* GOOGLE MAP CONTROLS EVENTS */

    // Zoom functie
    $('#gmapzoomIn').click(function () {
        ZoomIn();
    });

    $('#gmapzoomOut').click(function () {
        ZoomOut();
    });

    // street view
    $('#street-view').click(function () {
        toggleStreetView();
    });

    // map types
    $('#roadMap').click(function () {
        $('#view-weergave').html('<i class="fa  fa-picture-o"></i> Weergave');
        map.setMapTypeId(google.maps.MapTypeId.ROADMAP);
    });
    $('#terrain').click(function () {
        $('#view-weergave').html('<i class="fa  fa-picture-o"></i> TERRAIN');
        map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
    });
    $('#satellite').click(function () {
        $('#view-weergave').html('<i class="fa  fa-picture-o"></i> SATELLITE');
        map.setMapTypeId(google.maps.MapTypeId.SATELLITE);
    });
    $('#hybrid').click(function () {
        $('#view-weergave').html('<i class="fa  fa-picture-o"></i> HYBRID');
        map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    });
    console.log("details loaded correctly.");
});
