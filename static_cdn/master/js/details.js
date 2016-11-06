/**
 * Created by Sami on 17/05/2016.
 */

$( document ).ready(function() {
    likePand();
    function likePand() {
        $( "a" ).each(function( index ) {
            console.log("test = " + $(this).attr('data-val'));
            if ($(this).attr('data-val') != undefined && $.cookie($(this).attr('data-val')) != undefined) {
                $(this).children().addClass("isFavorite");
            }
        })
        $('a').click(function(e) {
            if ($(this).attr('data-val') != undefined && $.cookie($(this).attr('data-val')) == undefined) {
                $.cookie($(this).attr('data-val'), $(this).attr('data-val'),  { path: '/' });
                $(this).children().addClass("isFavorite");
                $.notify({
                    title: "Notificatie:",
                    message: "Pand is succesvol toegevoegd aan favorieten!",
                });
                e.preventDefault();
            } else if ($(this).attr('data-val') != undefined && $.cookie($(this).attr('data-val')) != undefined) {
                $.removeCookie($(this).attr('data-val'),  { path: '/' });
                $(this).children().removeClass("isFavorite");
                $.notify({
                    title: "Notificatie:",
                    message: "Pand is succesvol verwijderd van je favorieten!",
                });
                e.preventDefault();
            }
        });
    }
    console.log("details loaded correctly.");
});
