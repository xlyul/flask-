function logout() {
    $.get("/user/logout", function (data) {
        if (data.code == '200') {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function () {
    $.ajax({
        url: '/user/user/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.code == '200') {
                console.log(data);
                $('#user-mobile').html(data.user.phone);
                $('#user-name').html(data.user.name);
                $('#user-avatar').attr('src', data.user.avatar)
            }
        },
        error: function () {
            alert('请求失败！')
        }
    })
});