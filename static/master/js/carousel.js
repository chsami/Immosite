$( document ).ready(function() {
    console.log($('.item.active').children().size());
    hideCarouselImagesOnPageLoad();
    showCarouselImages(3);
});


function hideCarouselImagesOnPageLoad() {
    $('.item.active').children('div').each(function(i) {
        $($(this)).css({"visibility":"hidden"});
    });
}

function showCarouselImages(amount) {
    if ($('.item.active').children().size() > amount) {
        var timesLooped = 1;
        $('.carousel-inner').children('.item.notactive').each(function(i) {
            var amt = 0;
            var itemToAppend = $(this);
            $('.item.active').children('div').each(function (i) {
                if (amt > 2 * timesLooped && amt < 3*timesLooped+3) {
                    $(this).appendTo(itemToAppend);
                    $(this).css({"visibility": "visible"});
                } else {
                    $(this).css({"visibility": "visible"});
                    console.log("outside : " + amt);
                }
                amt++;
            });
            console.log("times looped : " + timesLooped)
            timesLooped++;
        });
    } else {
        $('.item.active').children('div').each(function (i) {
            $(this).css({"visibility": "visible"});
        });
    }
}

$('.multi-item-carousel').carousel({
        interval: false
    });

// for every slide in carousel, copy the next slide's item in the slide.
// Do the same for the next, next item.
$('.multi-item-carousel .item').each(function () {
    var next = $(this).next();
    if (!next.length) {
        next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));

    if (next.next().length > 0) {
        next.next().children(':first-child').clone().appendTo($(this));
    } else {
        $(this).siblings(':first').children(':first-child').clone().appendTo($(this));
    }
});