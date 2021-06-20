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


$("#add").click(function (){

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var pid = $('#product_id').val()
    var qty = $('#quantity').val()
    var order_id = $('#order_id').val()

    $.ajax({
        type: "POST",
        url: "/show_added_products_sales",
        data:{
            "product_id": pid,
            "quantity": qty,
            "order_id": order_id
        }, success: function (data){

            var instance = data;
            $("#total_amount").val(instance.total_sales_amount)
            $("#showdata tbody").prepend(
                `<tr>
                    <td>${instance.product_id || ""}</td>
                    <td>${instance.pname || ""}</td>
                    <td>${instance.price || ""}</td>
                    <td>${instance.quantity || ""}</td>
                    <td>${instance.sales_return_amount || ""}</td>
                </tr>`
            )
            console.log(data)
        },
    })
})