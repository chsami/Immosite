$( document ).ready(function() {
    var changePasswordForm = $("#change-password-form");
    changePasswordForm.submit(function(e) {
        $('body').css('cursor', 'wait');
        $('#change-password-form > p').text('Even geduld...');
        e.preventDefault();
        var formData = changePasswordForm.serialize();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url:'../profile/',
            type:'POST',
            data:formData,
            //data: {csrfmiddlewaretoken: token, formdata: formData},
            success:function(data) {
                if (data['error'] != undefined) {
                    $('#change-password-form').prepend(
                        '<div style="text-align:center; font-size: 1.4em;"class="alert alert-danger">' +
                        '' + data['error'] + '' +
                        '</div>'
                    );
                    $('#change-password-form > p').text('');
                } else {
                    $('#change-password-form').prepend(
                        '<div style="text-align:center; font-size: 1.4em;" class="alert alert-success">' +
                        '' + data['success'] + '' +
                        '</div>'
                    );
                     $('#change-password-form > p').text('');
                    $('#change-password-form > input[type=text]').val('');
                    $('#change-password-form > input').css('background-color', 'white');
                }
                $('body').css('cursor', 'default');
            },
            error: function (data) {
                console.log(data['error']);
                $('#change-password-form > p').append('Er is een fout opgetreden!');
                $('body').css('cursor', 'default');
            }
        });
    });

    $("input[name=new-password-confirmation]" ).keyup(function() {
        if ($(this).val() == $("input[name=new-password]").val()) {
            $(this).css('outline-color', 'rgba(0, 255, 0, 0.6)');
            $("input[name=new-password]").css('outline-color', 'rgba(0, 255, 0, 0.6)');
        } else {
            $(this).css('outline-color', 'rgba(255, 0, 0, 0.6)');
            $("input[name=new-password]").css('outline-color', 'rgba(255, 255, 0, 0.6)');
        }
    });

});