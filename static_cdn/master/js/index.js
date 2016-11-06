/**
 * Created by Sami on 19/05/2016.
 */
$( document ).ready(function() {
    var pand_counter = 0;
    loadFeaturedPanden();
    loadFavorietePanden();
    $('.btn-te-koop').css('background-color', '#0d3532');
    var cities = [];
    var postals = [];
    var pand_url = $('input[name=hidden-pand-url]').val();
    var media_url = $('input[name=hidden-media-url]').val();
    var favoriete_url = $('input[name=hidden-favorite-url]').val();
    function getAllSupportedItems() {
        return $.getJSON("../static/master/js/suggestions.json").then(function (data) {
            return data;
        });
    }

    var substringMatcher = function (strs) {
        return function findMatches(q, cb) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strs, function (i, str) {
                if (substrRegex.test(str)) {
                    matches.push(str);
                }
            });
            cb(matches);
        };
    };
    getAllSupportedItems().done(function (items) {
        for (i = 0; i < items.length - 1; i++) {
            if (items[i]['FIELD3'] != undefined)
                cities.push(items[i]['FIELD2'] + " " + items[i]['FIELD3']);
        }
        var unique_cities = cities.filter(function (itm, i, a) {
            return i == a.indexOf(itm);
        });
        ;
        $('#cities, #cities_adv').typeahead({
            highlight: true
        }, {
            name: 'cities',
            source: substringMatcher(unique_cities),
            limit: 5
        });
    });

    $('label').on('click', function () {
        if ($(this).attr('id') == 'id-lbl-huur') {
            $(this).hide().fadeIn();
            $('.normal-form').attr('action', 'panden/huur/');
            $('.advanced-form').attr('action', 'panden/huur/');
            $('.btn-te-koop').css('background-color', 'rgba(0, 0, 0, 0.6)');
            $(this).css('background-color', '#0d3532');
            $('#price-min-id').val(0);
            $('#price-max-id').val(50000);
            $( "#price-range-min" ).text(0);
            $( "#price-range-max" ).text(50000);
            $("#price-range-min").number( true, 0 );
            $("#price-range-max").number( true, 0 );
            $('#min-prijs').empty();
            $('#max-prijs').empty();
            $('#min-prijs').append('' +
                '<li>€400+</li>' +
                '<li>€500+</li>' +
                '<li>€600+</li>' +
                '<li>€700+</li>' +
                '<li>€800+</li>' +
                '<li>€900+</li>' +
                '<li>€1000+</li>' +
                '<li>€1500+</li>' +
                '<li>€2000+</li>' +
                '<li>€3000+</li>'
            );
            $('#max-prijs').append('' +
                '<li>€400</li>' +
                '<li>€500</li>' +
                '<li>€600</li>' +
                '<li>€700</li>' +
                '<li>€800</li>' +
                '<li>€900</li>' +
                '<li>€1000</li>' +
                '<li>€1500</li>' +
                '<li>€2000</li>' +
                '<li>€3000</li>'
            );
        } else if ($(this).attr('id') == 'id-lbl-koop') {
            $(this).hide().fadeIn();
            $('.normal-form').attr('action', 'panden/koop/');
            $('.advanced-form').attr('action', 'panden/koop/');
            $('.btn-te-huur').css('background-color', 'rgba(0, 0, 0, 0.6)');
            $(this).css('background-color', '#0d3532');
            $('#price-min-id').val(0);
            $('#price-max-id').val(5000000);
            $( "#price-range-min" ).text(0);
            $( "#price-range-max" ).text(5000000);
            $("#price-range-min").number( true, 0 );
            $("#price-range-max").number( true, 0 );
            $('#min-prijs').empty();
            $('#max-prijs').empty();
            $('#min-prijs').append('' +
                '<li>€100.000+</li>' +
                '<li>€150.000+</li>' +
                '<li>€200.000+</li>' +
                '<li>€250.000+</li>' +
                '<li>€300.000+</li>' +
                '<li>€400.000+</li>' +
                '<li>€500.000+</li>' +
                '<li>€600.000+</li>' +
                '<li>€700.000+</li>' +
                '<li>€800.000+</li>'
            );
            $('#max-prijs').append('' +
                '<li>€100.000+</li>' +
                '<li>€150.000+</li>' +
                '<li>€200.000+</li>' +
                '<li>€250.000+</li>' +
                '<li>€300.000+</li>' +
                '<li>€400.000+</li>' +
                '<li>€500.000+</li>' +
                '<li>€600.000+</li>' +
                '<li>€700.000+</li>' +
                '<li>€800.000+</li>'
            );

        }
    });

    $('.property-search-feature').on('click', function () {
        if ($(this).attr('clicked') == 'true') {
            $(this).attr('clicked', 'false');
            $(this).attr('value', '');
        } else {
            $(this).attr('clicked', 'true');
            $(this).attr('value', $(this).attr('name'));
        }
        console.log($(this).attr('clicked'));
    });
    //Check to see if the window is top if not then display button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    //Click event to scroll to top
    $('.scrollToTop').click(function () {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
    function loadFeaturedPanden() {
        $('#form-load-panden').on('submit', function (e) {
            e.preventDefault();
            var token = $('input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url: "#",
                type: 'POST',
                data: {csrfmiddlewaretoken: token},
                success: function (data) {
                    if (data != undefined && data.length > 0) {
                        $('#featured_property > .carousel-inner > .active').empty();
                        initTemplateData(data, true, 'featured_property', 'In de kijker');
                    }
                },
                error: function (data) {
                    console.log("error");
                }
            });
        });
        $('#form-load-panden').trigger("submit");
    }

    function loadFavorietePanden() {
        $('#favorite-panden-form').on('submit', function (e) {
            e.preventDefault();
            var token = $('input[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url: "#",
                type: 'POST',
                data: {csrfmiddlewaretoken: token},
                success: function (data) {
                    if (data != undefined && data.length > 0) {
                       $('#favorite_property > .carousel-inner > .active').empty();
                        aantal_panden = initTemplateData(data, false, 'favorite_property', '');
                        likePand();
                        $('[data-toggle="tooltip"]').tooltip();
                        if (aantal_panden <= 0) {
                            $('#favorite_property').empty();
                        }
                    }

                },
                error: function (data) {
                    console.log("error");
                }
            });
        });
        $('#favorite-panden-form').trigger("submit");
       // $('#form-load-panden').trigger("submit");
    }


    function loadPandTemplate(referentienummer, type, stad, straat, postcode, status,
                              profiel_foto, inkijker, oppervlakte, aantal_kamers, aantal_slaapkamers,
                                aantal_badkamers, prijs, huisnummer, heartIcon, naam_slaapkamer, naam_badkamer,
                              beschrijving) {
        if (inkijker != '') {
            inkijker = ' <div class="featured_div">' +
            ' <span>' + inkijker + '</span>' +
            '</div>';
        }
        if (heartIcon) {
            heartIcon = '<a class="" href="#" data-val="' + referentienummer + '">' +
            '<i class="glyphicon glyphicon-heart" data-toggle=""' +
            'title="Toevoegen aan favoriet"></i>' +
            '</a>';
        } else {
            heartIcon = '♥';
        }
        var kamer_naam = '';
        if (location.pathname === '/nl/') {
            kamer_naam = "Kamer(s)";
        } else if (location.pathname === '/en/') {
            kamer_naam = "Chamber(s)"
        } else if (location.pathname === '/fr/') {
            kamer_naam = "Chambre(s)"
        }
        return '<li class="col-sm-6 col-md-4 col-lg-4 property-list-area primary-tooltips">' +
        '<div class="property-list-grid">' +
        '<a href="' + pand_url + '' + referentienummer + '">' +
        '<div class="photo">' +
        '<div class="property-title" data-toggle="tooltip" data-placement="top" title="">' +
        '<h3 class="title">' + type + ' in '  + stad + '</h3>' +
        '<h4 class="address">' + straat + ' ' + huisnummer + ', ' + postcode + ' ' + stad + ', België</h4>' +
        '</div>' +
        '</a>' +
        '<div class="property-image">' +
        '<a href="#">' +
        '<img src=' + media_url +
        '' + profiel_foto + ' class="img-responsive" style="height:40%;" alt="a" />' +
        '<label>' + status + '</label>' +
        '<figcaption>' +
        '<div class="property-short-description">' +
        '<div class="subtitle ">' +
        '<span class="type">' + type + '</span>' +
        '<span>·</span>' +
        '<span class="status">in ' + stad + '</span>' +
        '</div>' +
        '<p>' + beschrijving + '</p>' +
        '</div></figcaption></a>' +
        '' + inkijker + '' +
        '</div>' +
        '<div class="property-content">' +
        '<div class="property-meta clearfix">' +
        '<div>' +
        '<div class="meta-title"><i class="fa fa-expand"></i></div>' +
        '<div class="meta-data" data-toggle="tooltip" title=""data-original-title="oppervlakte">' + oppervlakte +
        'm<sup>2</sup> </div>' +
        '</div>' +
        '<div>' +
        '<div class="meta-title"><i class="fa fa-building-o"></i></div>' +
        '<div class="meta-data" data-toggle="tooltip" title=""data-original-title="Kamers">' + aantal_kamers +
        ' ' + kamer_naam + ' </div>' +
        '</div>' +
        '<div>' +
        '<div class="meta-title"><i class="glyphicon glyphicon-bed"></i></div>' +
        '<div class="meta-data" data-toggle="tooltip" title=""data-original-title="Slaapkamers">' + aantal_slaapkamers +
        ' ' + naam_slaapkamer + ' </div>' +
        '</div>' +
        '<div>' +
        '<div class="meta-title"><i class="fa fa-tint"></i></div>' +
        '<div class="meta-data" data-toggle="tooltip" title=""data-original-title="Badkamer">' + aantal_badkamers +
        ' ' + naam_badkamer + ' </div> </div>' +
        '</div>' +
        '<div class="property-price">' +
        '' + heartIcon + '' +
        '<div class="price-tag" data-toggle="tooltip" title="prijs">&euro; ' + $.number( prijs, 0 ) +
        '<div class="clearfix"></div>' +
        '</div>' +
        '</div>' +
        '</li>'
    }

    function initTemplateData(data, cookie, id, inkijker) {
        var aantal_panden = 0;
        var counter = 0;
        var aantal_panden = 0;
        var oppervlakte = 0;
        var aantal_slaapkamers = 0;
        var aantal_badkamers = 0;
        var criteria_slaapkamer = '';
        var criteria_badkamer = '';
        for (i = 0; i < data.length; i++) {
            if ($.cookie(data[i]['fields']['referentienummer']) != undefined || cookie) {
                if (data[i]['model'] === "master.pand") {
                    for (x = 0; x < data.length; x++) {
                        if (data[x]['model'].indexOf("type") >= 0) {
                            if (data[i]['fields']['type'] == data[x]['pk']) {
                                if (location.pathname === '/nl/') {
                                    data[i]['fields']['type'] = data[x]['fields']['naam'];
                                } else if (location.pathname === '/en/') {
                                    data[i]['fields']['type'] = data[x]['fields']['naam_en'];
                                } else if (location.pathname === '/fr/') {
                                    data[i]['fields']['type'] = data[x]['fields']['naam_fr'];
                                }
                            }
                        } else if (data[x]['model'].indexOf("pandeigenschap") >= 0) {
                            if (data[i]['pk'] == data[x]['fields']['pand']) {
                                oppervlakte = data[x]['fields']['oppervlakte'];
                            }
                        } else if (data[x]['model'].indexOf("status") >= 0) {
                            if (data[i]['fields']['status'] == data[x]['pk']) {
                                if (location.pathname === '/nl/') {
                                    data[i]['fields']['status'] = data[x]['fields']['naam'];
                                } else if (location.pathname === '/en/') {
                                    data[i]['fields']['status'] = data[x]['fields']['naam_en'];
                                } else if (location.pathname === '/fr/') {
                                    data[i]['fields']['status'] = data[x]['fields']['naam_fr'];
                                }
                            }
                        } else if (data[x]['model'].indexOf("pandcriteria") >= 0) {
                            for (z = 0; z < data.length; z++) {
                                if (data[z]['model'] === "master.criteria") {
                                    if (data[z]['pk'] == data[x]['fields']['criteria']) {
                                        if (data[z]['fields']['naam'].toLowerCase().indexOf("slaap") >= 0) {
                                            if (location.pathname === '/nl/') {
                                            criteria_slaapkamer = data[z]['fields']['naam'];
                                            } else if (location.pathname === '/en/') {
                                                criteria_slaapkamer = data[z]['fields']['naam_en'];
                                            } else if (location.pathname === '/fr/') {
                                                criteria_slaapkamer = data[z]['fields']['naam_fr'];
                                            }
                                            aantal_slaapkamers = data[x]['fields']['aantal'];
                                        } else if (data[z]['fields']['naam'].toLowerCase().indexOf("bad") >= 0) {
                                            if (location.pathname === '/nl/') {
                                                criteria_badkamer = data[z]['fields']['naam'];
                                            } else if (location.pathname === '/en/') {
                                                criteria_badkamer = data[z]['fields']['naam_en'];
                                            } else if (location.pathname === '/fr/') {
                                                criteria_badkamer = data[z]['fields']['naam_fr'];
                                            }
                                            aantal_badkamers = data[x]['fields']['aantal'];
                                        }
                                    }
                                }
                            }
                        }
                    }
                    aantal_panden++;
                    if (i < 3) {
                        $('#' + id + ' > .carousel-inner > .active').append(
                            loadPandTemplate(data[i]['fields']['referentienummer'],
                                            data[i]['fields']['type'],
                                            data[i]['fields']['stad'],
                                            data[i]['fields']['straat_naam'],
                                            data[i]['fields']['postcode'],
                                            data[i]['fields']['status'],
                                            data[i]['fields']['profiel_foto'],
                                            inkijker,
                                            oppervlakte,
                                            data[i]['fields']['aantal_kamers'],
                                            aantal_slaapkamers,
                                            aantal_badkamers,
                                            data[i]['fields']['prijs'],
                                            data[i]['fields']['huis_nummer'],
                                            cookie,
                                            criteria_slaapkamer,
                                            criteria_badkamer,
                                            data[i]['fields']['beschrijving']
                            )
                        );
                    } else if (i % 3 == 0) {
                        counter++;
                        $('#' + id + ' > .carousel-inner').append('<div class="item pand-' + counter + '">' +
                            loadPandTemplate(data[i]['fields']['referentienummer'],
                                            data[i]['fields']['type'],
                                            data[i]['fields']['stad'],
                                            data[i]['fields']['straat_naam'],
                                            data[i]['fields']['postcode'],
                                            data[i]['fields']['status'],
                                            data[i]['fields']['profiel_foto'],
                                            inkijker,
                                            oppervlakte,
                                            data[i]['fields']['aantal_kamers'],
                                            aantal_slaapkamers,
                                            aantal_badkamers,
                                            data[i]['fields']['prijs'],
                                            data[i]['fields']['huis_nummer'],
                                            cookie,
                                            criteria_slaapkamer,
                                            criteria_badkamer,
                                            data[i]['fields']['beschrijving']
                            )
                        );
                    } else {
                        $('#' + id + ' > .carousel-inner > .pand-' + aantal_panden).append(
                            loadPandTemplate(data[i]['fields']['referentienummer'],
                                            data[i]['fields']['type'],
                                            data[i]['fields']['stad'],
                                            data[i]['fields']['straat_naam'],
                                            data[i]['fields']['postcode'],
                                            data[i]['fields']['status'],
                                            data[i]['fields']['profiel_foto'],
                                            inkijker,
                                            oppervlakte,
                                            data[i]['fields']['aantal_kamers'],
                                            aantal_slaapkamers,
                                            aantal_badkamers,
                                            data[i]['fields']['prijs'],
                                            data[i]['fields']['huis_nummer'],
                                            cookie,
                                            criteria_slaapkamer,
                                            criteria_badkamer,
                                            data[i]['fields']['beschrijving']
                            )
                        );
                    }
                }
            }
        }
        return aantal_panden;
    }

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

    function preSearch() {

    }
});