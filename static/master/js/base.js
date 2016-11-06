$( document ).ready(function() {
     loadUI();
    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        options.async = true; //make the login and register page load async
    });
    var cities = [];
    var postals = [];
    function getAllSupportedItems() {
        return $.getJSON("/static/master/js/suggestions.json").then(function (data) {
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
    $('#login_link').on('click', function (event) {
        $('h4').html('Login');
        var lang = "nl";
		//$('#main-background').css('-webkit-filter', 'blur(5px)');
			$('#model-body-content').empty();
            if (location.pathname.length == 4) {
				url = "login/"
			} else if ((location.pathname.split("/").length - 1) == 3) {
				url = "../login/"
			} else if ((location.pathname.split("/").length - 1) == 4) {
				url = "../../login/"
			} else if ((location.pathname.split("/").length - 1) == 5) {
				url = "../../../login/"
			}
			$("#model-body-content").load(url + " .container-fluid", function() {
				$('#login-message').html("");
				$.getScript("/static/master/js/login.js")
				  .done(function( script, textStatus ) {
					console.log( textStatus );
				  })
				  .fail(function( jqxhr, settings, exception ) {
					console.log( "Triggered ajaxError handler." );
				});
			});
		$('#mainModal').modal();
        event.preventDefault();
    });

    function findTextInNavBar(text) {
        $(".nav li a").each(function(key, value) {
            if ($(value).text() == text) {
                $(value).css('text-decoration', 'underline');
            }
        });
    }

    $('a').on('click', function() {
        $.cookie('page', $(this).text(), { path: '/' });
    });

    /*Amara hippie code*/

	 $(document).on('click', '#min-prijs li', function() {
        $('#min-datebox').val($(this).text());
    });
    $(document).on('click', '#max-prijs li', function() {
        $('#max-datebox').val($(this).html());
    });

    $("#opties").on("hide.bs.collapse", function(){
        $(".btn-opties").html('<span class="glyphicon glyphicon glyphicon-chevron-down"></span> Meer opties');
    });
    $("#opties").on("show.bs.collapse", function(){
        $(".btn-opties").html('<span class="glyphicon glyphicon-chevron-up"></span> Minder opties');
    });

    $('#support-ticket-div').click(function(event) {
        $('#support-ticket-form').fadeIn();
        $(this).fadeOut();
    });

    $('#close-support-ticket-form').click(function() {
        $('#support-ticket-form').fadeOut();
        $('#support-ticket-div').fadeIn();
    });

    $(document).mouseup(function (e) { //als we buiten de form klikken dan gaan we de form verbergen
        var container = $("#support-ticket-form");
        if (container.is(':visible') && !container.is(e.target) && container.has(e.target).length === 0) {
            container.fadeOut();
            $('#support-ticket-div').fadeIn();
        }
    });

    var ticketForm = $("#support-ticket-form");
    ticketForm.submit(function(e) {
        $('body').css('cursor', 'wait');
        $('#support-ticket-form > center > p').append('Even geduld...');
        e.preventDefault();
        var formData = ticketForm.serialize();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url:'admin-support-ticket/',
            type:'POST',
            data:formData,
            //data: {csrfmiddlewaretoken: token, formdata: formData},
            success:function(data) {
                $('#support-ticket-form > center > p').text('Bericht is succesvol verstuurd!');
                $('#support-ticket-form > center > textarea').val('');
                $('#support-ticket-form > center > input').val('');
                $('body').css('cursor', 'default');
            },
            error: function (data) {
                $('#support-ticket-form > p').append('Er is een fout opgetreden!');
                $('body').css('cursor', 'default');
            }
        });
    });

    loadLanguage();
    function loadLanguage() {
        if ($.cookie('lang') == 'en') {
            $('.btn-dropdown-languages').empty();
            $('.btn-dropdown-languages').append('<span class="lang-sm lang-lbl-full" ' +
                'lang="en"></span> <span class="caret"></span>');
          // window.location.href = "http://" +window.location.host + "/en";
            //$.cookie('lang', $(this).attr("en"));
        } else if ($.cookie('lang') == 'fr') {
          $('.btn-dropdown-languages').empty();
            $('.btn-dropdown-languages').append('<span class="lang-sm lang-lbl-full" ' +
                'lang="fr"></span> <span class="caret"></span>');;
        } else if ($.cookie('lang') == 'nl') {
            $('.btn-dropdown-languages').empty();
            $('.btn-dropdown-languages').append('<span class="lang-sm lang-lbl-full" ' +
                'lang="nl"></span> <span class="caret"></span>');
            //window.location.href = "http://" + window.location.host + "/nl";
           // $.cookie('lang', $(this).attr("nl"));
        }
    }
    chooseLanguage();
    function chooseLanguage() {
        $('.dropdown-menu-languages > li > a').on('click', function() {
            $('.btn-dropdown-languages').empty();
            $('.btn-dropdown-languages').append('<span class="lang-sm lang-lbl-full" ' +
                'lang=' + $(this).attr("lang") + '></span> <span class="caret"></span>');
             $.cookie('lang', $(this).attr("lang"), { path: '/' });
             window.location.href = "http://" + window.location.host + "/" + $(this).attr("lang");
            console.log(window.location.href);
        });
    }
    if ($(document).find("title:contains('Home')").text()) {
        $.cookie('page', '', { path: '/' });
    }
    findTextInNavBar($.cookie('page'), { path: '/' });


    /**
     * ADVANCED SEARCH SLIDER - > INHERITS FROM JQUERY.UI
     */

        var min = 50;
        var max = 10000;
        var steps = 1000;
        $('#size-min-id').val(min);
        $('#size-max-id').val(max);
        $("#slider-size").slider({
            range: true,
            min: min,
            max: max,
            steps: steps,
            values: [min, max],
            slide: function (event, ui) {
                $("#size-range-min").text(ui.values[0]);
                $("#size-range-max").text(ui.values[1]);
                $('#size-min-id').val(ui.values[0]);
                $('#size-max-id').val(ui.values[1]);
            }
        });
        $("#size-range-min").text($("#slider-size").slider("values", 0));
        $("#size-range-max").text($("#slider-size").slider("values", 1));

    console.log("Base.js loaded correctly.");
});

 function loadUI() {
        var min = 0;
        var steps = 1000;
        $("#slider-price").slider({
            range: true,
            min: min,
            max: $('#price-max-id').attr('value'),
            steps: steps,
            values: [min, $('#price-max-id').attr('value')],
            slide: function (event, ui) {
                $("#price-range-min").text(ui.values[0]);
                $("#price-range-max").text(ui.values[1]);
                $("#price-range-min").number(true, 0);
                $("#price-range-max").number(true, 0);
                $('#price-min-id').val(ui.values[0]);
                $('#price-max-id').val(ui.values[1]);
            }
        });

        $("#price-range-min").text($("#slider-price").slider("values", 0));
        $("#price-range-max").text($("#slider-price").slider("values", 1));
        $("#price-range-min").number(true, 0);
        $("#price-range-max").number(true, 0);
    }