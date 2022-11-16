$(document).ready(function(){
    if (window.location.pathname === '/')
    console.log("script hitted 'home'")
    var counter = 0;
    var cname= 'theme_container';
    $("div[class^='theme_container").each(function(){
        counter++;
        $(this).removeClass(cname);
        $(this).addClass(cname+counter);
    });
});


$(document).ready(function () {
    function getCookie(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != ''){
            var cookies = document.cookie.split(';');
            for (var i = 0; i< cookies.length; i++){
                var cookie = cookies[i].trim();

                if (cookie.substring(0, name.length +1) === (name + "=")){
                    cookieValue = decodeURIComponent(cookie.substring(name.length +1));
                    break;
                }
            }
        }
        return cookieValue;
    };
});

var csrftoken = getCookie('csrftoken')

function csrfSafeMethod(method){
    return ['GET', 'OPTIONS', 'HEAD', 'TRACE'].includes(method);
};

$.ajaxSetup({
    beforeSend: function(xhr, setting){
        if (!csrfSafeMethod(setting.type) && !this.crossDomain)
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }
});


    $(document).on('change', '.custom-select', function(e){
    var finition = [$('#select_finition').val(), $('#select_finition option:selected').text()];
    var size = [$('#select_size').val(), $('#select_size option:selected').text()];
    $.ajax({
        type:'POST',
        url: window.location.pathname,
        data: {
            'ajax_post': 'product-detail',
            'sent_finition' : finition,
            'sent_size': size,
        },
        success : function(response){
            var price = JSON.parse(response.price)
            if(price){
                $('#price_container').append(
                    `
                    <p><span>$</span>${price}</p>
                    `
                )
            };
        }
    })
});