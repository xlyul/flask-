function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$("#form-avatar").submit(function () {
    $(this).ajaxSubmit({
        url: '/user/user/',
        type: 'PUT',
        dataType: 'json',
        success: function (msg) {
            if (msg.code == '200') {
                $('#user-avatar').attr('src', msg.url)
            }
        },
        error: function (msg) {
            console.log(msg);
        }
    });
    return false
});

$('#form-name').submit(function () {
    $('.error-msg').hide();
    var name = $('#user-name').val();
    $.ajax({
        url: '/user/user/',
        type: 'PUT',
        data: {'name': name},
        dataType: 'json',
        success: function (msg) {
            if (msg.code != '200') {
                $('.error-msg').html('<i class="fa fa-exclamation-circle">'+ msg.msg +'</i>');
                $('.error-msg').show()
            }
        },
        error: function (msg) {
            alert('请求失败！')
        }
    });
    return false
});