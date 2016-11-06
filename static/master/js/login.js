/**
 * Created by Sami on 2/05/2016.
 */

	$( document ).ready(function() {
		handleLoginInput();
		var loginForm = $("#loginForm");
		loginForm.submit(function(e) {
			//console.log("clicked " + $('input[name=password]').val());
			$('body').css('cursor', 'wait');
			e.preventDefault();
			//var formData = loginForm.serialize();
			var token = $('input[name=csrfmiddlewaretoken]').val();
			var email = $('#loginForm > .col-md-6 > input[name=email]').val() == "" ? "null" : $('#loginForm > .col-md-6 > input[name=email]').val();
			var password = $('#loginForm > .col-md-6 > input[name=password]').val() == "" ? "null" : $('#loginForm > .col-md-6 > input[name=password]').val();
			console.log("location.protocol " + url + "  "  + location.pathname);
			if (location.pathname.length == 4) {
				url = "login/";
			} else if ((location.pathname.split("/").length - 1) == 3) {
				url = "../login/";
			} else if ((location.pathname.split("/").length - 1) == 4) {
				url = "../../login/";
			} else if ((location.pathname.split("/").length - 1) == 5) {
				url = "../../../login/";
			}
			$('#login-message').empty();
			$('#login-message').append('Even geduld...');
			$.ajax({
				url:url,
				type:'POST',
				//data:formData,
				data: {csrfmiddlewaretoken: token, email: email, password: password},
				success:function(data) {
					//console.log(data['error'].length);
					if (data['error'] != undefined) { //look if the error exists?
						$('#login-message').empty();
						$('#login-message').append(data['error']).hide().fadeIn();
					} else { //no error?
						location.reload();
					}
					$('body').css('cursor', 'default');
				},
				error: function (data) {
					console.log("error");
					$('body').css('cursor', 'default');
				}
			});
		});
		console.log("Login.js loaded succesfully.");
	});

function handleLoginInput() {
	$('form input').focusout(function() {
		validationRules($(this));
	});
	$('form input').each(function() {
		$(this).keyup(function() {
			validationRules($(this));
		});
	});
	$('form input').change(function() {
		validationRules($(this));
	});
}

function validationRules(inputField) {
	switch (inputField.attr('name')) {
		case "email":
			return checkValidation(inputField, 2, 30, ['emailValidationRequired']);
	}
}




function checkValidation(inputField, min, max, checkArray) {
	var isValid = "";
	//console.log();
	//inputField length check
	isValid = inputField.val().length >= min && inputField.val().length <= max ? "correct" : "Veld moet tussen " + min + " en " + max + " karakters bevatten.";
	//only check other fields if the inputField is still valid
	if (isValid == "correct") {
		checkArray.forEach(function(val) {
			if (val == "containsNumberValidationRequired") {
				isValid = !stringContainsNumber(inputField.val()) ? "correct" : "Veld kan geen getallen bevatten.";
			} else if (val == "emailValidationRequired") {
				isValid = isValidEmailAddress(inputField.val()) ? "correct" : "email address invalid";
			} else if (val == "phoneValidationRequired") {
				isValid = isValidCellphone(inputField.val()) ? "correct" : "geen geldig gsm nummer";
			} else if (val == "numberValidationRequired") {
				isValid = $.isNumeric(inputField.val()) ? "correct" : "textveld kan geen letters of symbolen bevatten.";
			} else if (val == "alphaNumericValidationRequired") {
				isValid = alphaNumericOnly(inputField.val()) ? "correct" : "textveld kan geen symbolen bevatten.";
			} else if (val == "passwordMatchValidationRequired") {
				isValid = checkPasswordMatch(inputField.val()) ? "correct" : "Wachtwoord komt niet overeen.";
			} else if (val == "TODO") {
				isValid = "correct";
			}
		});
	}
	//make a choose depending on the validation
	if (isValid == "correct") {
		inputField.removeClass('invalidInput');
		inputField.addClass('validInput');
		//$('#notification').hide();
	} else {
		inputField.removeClass('validInput');
		inputField.addClass('invalidInput');
		//showNotification(isValid, inputField.offset());
	}
	return isValid;
}

function showNotification(error, position) {
	//$('#login-message').show();
	//$('#login-message p').text(error);

}

//Credits to : http://so.devilmaycode.it/jquery-validate-e-mail-address-regex/
function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
}