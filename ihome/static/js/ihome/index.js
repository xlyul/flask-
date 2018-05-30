//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function () {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/house/search/?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    // var areaName = $(th).attr("area-name");
    // if (undefined == areaName) areaName = "";
    // url += ("aname=" + areaName);
    // url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    var a = $(th).attr("area-id");
    var b = $(th).attr("start-date");
    var c = $(th).attr("end-date");
    if (a && b && c ){
        location.href = url;
    }
    else {
        alert('请填写完整搜索条件！')
    }

}

$(document).ready(function () {
    $(".top-bar>.register-login").show();


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function () {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.get('/house/index/', function (data) {

        if (data.code == '200') {
            var user_name_html = template('user_info_re_log',{user_name:data.user_name});
            $('.top-bar').append(user_name_html);

            if (data.user_name){
                $('.register-login').hide();
                $('.user-info').show();
            }
            else{
                $('.register-login').show();
                $('.user-info').hide()
            }

            var house_img = template('house-img', {ohouses: data.hlist});
            $('.swiper-wrapper').append(house_img);

            var area = template('area', {areas: data.area_list});
            $('.area-list').append(area)
        }
        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationClickable: true
        });
        $(".area-list a").click(function (e) {
            $("#area-btn").html($(this).html());
            $(".search-btn").attr("area-id", $(this).attr("area-id"));
            $(".search-btn").attr("area-name", $(this).html());
            $("#area-modal").modal("hide");
        });
    })
});


function logout() {
    $.get("/user/logout", function (data) {
        if (data.code == '200') {
            location.href = "/user/login/";
        }
    })
}