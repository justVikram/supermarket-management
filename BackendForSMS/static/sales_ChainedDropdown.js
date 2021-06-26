function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('#order_id').change(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })

    var order_id = $('#order_id').val()

    $.ajax({
        type: "POST",
        url: "/chaineddropdownsales",
        data:{
            "order_id": order_id,
        },
        success: function (data){
            console.log(data);

            // Add below snippet no
            let productSelectBox = $('#product_id');

            document.getElementById('product_id').innerText = null;

            const productsData = data.SortByOrder;
            $.each(productsData, function(idx, product) {
                let productOption = $("<option/>", {
                    value: product.product_id,
                    text: product.product_id
                });

                productSelectBox.append(productOption);
            });
        }
    })
});