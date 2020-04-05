$(document).ajaxError(function (event, jqxhr, settings, thrownError) {

    // console.log(event)
    // console.log(jqxhr)
    // console.log(settings)
    // console.log(thrownError)
    if(jqxhr.status==318){ //代表未登录
        data = jqxhr.responseJSON;
        // 获取要跳转的地址
        url = data.url;
        // 跳转到要登录的界面
        window.location.href="/?url=" + encodeURI(url)
    }
});
