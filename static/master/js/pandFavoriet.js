/**
 * Created by Sami on 17/05/2016.
 */

$(document).ready(function () {
    loadFavoritePanden();
    function loadFavoritePanden() {
        $('#submit-favorite-panden-form').on("click", function(e) {
             e.preventDefault();
            var favorietePanden = getFavoritePanden();
            console.log("Loading favorite panden....");
            console.log(favorietePanden);
            var token = $('#favorite-panden-form > input[name=csrfmiddlewaretoken]').val();
            var media_url = $('input[name=hidden-media-url]').val();
            var pand_url = $('input[name=hidden-pand-url]').val();
            $.ajax({
                url: "nl/favoriete/",
                type: 'POST',
                //data:formData,
                data: {csrfmiddlewaretoken: token, favorietePanden: favorietePanden},
                success: function (data) {
                    var char = "-";
                    data = data.split(",");
                    for(x = 0; x < data.length - 1;x++) {
                        var referentienummer = data[x].split(char)[0];
                        var profiel_foto = data[x].split(char)[1];
                        var type = data[x].split(char)[2];
                        var status = data[x].split(char)[3];
                        var straat = data[x].split(char)[4];
                        var stad = data[x].split(char)[5];
                        var prijs = data[x].split(char)[6];
                        $('#jquery-container-placer').append('<div class="col-sm-4">' +
                            '<div class="pop-pand-lijst">' +
                            '<div id = pop-pand-item-' + x + ' class="pop-pand-item">'
                        );
                        $('#jquery-container-placer #pop-pand-item-' + x).append('<div class="hero">' +
                            '<a href=' + pand_url + '' + referentienummer + ' class="link"></a>' +
                            '<div class="images">' +
                            '<div class="images-container"><img data-id="avatar" class="image-responsive" src=' + media_url +
                            '' + profiel_foto + ' alt="">' +
                            '<ul class="label-group">' +
                            '<li><div data-type="label" class="label-price"> € ' + prijs + '</div></li>' +
                            '<div class="overlay"> <ul class="make-favo">'
                        );
                        $('#jquery-container-placer #pop-pand-item-' + x).append(
                            '<div class="body"><a data-id="link" href="#" class="link"></a>' +
                            '<div class="pand-type truncate"> <i class="glyphicon glyphicon-asterisk way sale"></i>' +
                            '<span class="type truncate">' + type + ' ' + status + '</span></div>' +
                            '<div class="adress truncate"> <a href="#">' + straat + ' - ' + stad + '</a></div>' +
                            '<div class="details truncate">'+
                            '<span class="fa fa-circle bedden"  aria-hidden="true"> STRAAT</span>'+
                            '<span class="fa fa-circle gebied" aria-hidden="true"> 120m<sup>2</sup></span>'
                        );

                        //$('#image-holder').append('<img id="fav-image" data-id="avatar" class="image-responsive"  src= ' +
                            //$("input[name=hidden-media-url]").val() + '' + data[x].split(/ +/)[1] + '  alt="">');
                    }
                    console.log("it was a succes.");
                },
                error: function (data) {
                    console.log("error");
                }
            });
        });
        $('#submit-favorite-panden-form').trigger("click");
    }

    function getFavoritePanden() {
        var list = [];
        $('.favorite_pand_link').each(function (key, val) {
            href = $(this).attr('href').split('/');
            if ($.cookie(href[3]) != undefined) {
                list += $.cookie(href[3]) + " "
                $(this).addClass('isFavorite');
                console.log(list);
            }
        });
        return list;
    }





    var link = $(".favorite_pand_link");
    var btn_add = $('#add_favorites > a');
    var btn_delete = $('#remove_favorites > a');
    btn_delete.on('click', function (e) {
        e.preventDefault();
        var url = window.location.pathname;
        var pk = url.substr(url.length - 2).substr(0, 1);
        var url = pk;

        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: "/favoriete/" + url + "/",
            type: 'POST',
            //data:formData,
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: function (data) {
                console.log(data);
                $('#remove_favorites > a').each(function (key, val) {
                    if ($(this).attr('href') == "/favoriete/" + url + "/") {
                        if (data['add_to_favorite'] == true) {
                            $(this).text('Verwijder van favorieten');
                            $(this).append('<input type="hidden" name="csrfmiddlewaretoken" value=' + token + '>');
                        } else {
                            $(this).text('Voeg to aan favorieten');
                            $(this).append('<input type="hidden" name="csrfmiddlewaretoken" value=' + token + '>');
                        }
                    }
                });
            },
            error: function (data) {
                console.log("error");
            }
        });
    });
    //details page
    btn_add.on('click', function (e) {
        console.log("clicked on it!");
        //console.log("clicked " + $('input[name=password]').val());
        e.preventDefault();
        var url = window.location.pathname;
        var pk = url.substr(url.length - 2).substr(0, 1);
        var url = pk;
        console.log(pk);
        //var formData = loginForm.serialize();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        //var email = $('input[name=email]').val() == "" ? "null" : $('input[name=email]').val();
        //var password = $('input[name=password]').val() == "" ? "null" : $('input[name=password]').val();
        //console.log(token + " : " + email + " : " + password);
        $.ajax({
            url: "/favoriete/" + url + "/",
            type: 'POST',
            //data:formData,
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: function (data) {
                $('#add_favorites > a').each(function (key, val) {
                    if ($(this).attr('href') == "/favoriete/" + url + "/") {
                        if (data['add_to_favorite'] == true) {
                            $(this).text('Verwijder van favorieten');
                            $(this).append('<input type="hidden" name="csrfmiddlewaretoken" value=' + token + '>');
                        } else {
                            $(this).text('Voeg to aan favorieten');
                            $(this).append('<input type="hidden" name="csrfmiddlewaretoken" value=' + token + '>');
                        }
                    }
                });
            },
            error: function (data) {
                console.log("error");
            }
        });
    });
    //index page
    link.on('click', function (e) {
        //console.log("clicked " + $('input[name=password]').val());
        e.preventDefault();
        var url = $(this).attr('href');
        console.log(url);
        url = url.split('/');
        pk = url[3];
        url = url[3];
        console.log(url);
        var token = $('input[name=csrfmiddlewaretoken]').val();
            if ($.cookie(url) == undefined) {
                $.cookie(url, pk);
                $(this).addClass('isFavorite');
                $.notify({
                    title: "Notificatie:",
                    message: "Pand is succesvol toegevoegd aan favorieten!",
                });
            } else {
                $.notify({
                    title: "Notificatie:",
                    message: "Pand is succesvol verwijderd van favorieten!",
                });
                $.removeCookie(url);
                $(this).removeClass('isFavorite');
            }
        /*$.ajax({
         url: url,
         type:'POST',
         //data:formData,
         data: {csrfmiddlewaretoken: token, pk: pk},
         success:function(data) {
         $('.favorite_pand_link').each(function(key, val) {
         if ($(this).attr('href') == url) {
         if (data['add_to_favorite'] == true) {
         $(this).addClass('isFavorite');
         } else {
         $(this).removeClass('isFavorite');
         }
         }
         });
         },
         error: function (data) {
         console.log("error");
         }
         });*/
    });
    console.log("pandFavoriet.js loaded succesfully.");
});