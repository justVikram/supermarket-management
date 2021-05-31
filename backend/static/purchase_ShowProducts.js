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
    var batch_no = $('#batch_no').val()

    $.ajax({
        type: "POST",
        url: "/show_added_products_purchase",
        data:{
            "product_id": pid,
            "batch_no": batch_no
        }, success: function (data){

            var instance = data;
            $("#amount_returned").val(instance.total_purchase_amount)
            $("#showdata tbody").prepend(
                `<tr>
                    <td>${instance.product_id || ""}</td>
                    <td>${instance.pname || ""}</td>
                    <td>${instance.price || ""}</td>
                    <td>${instance.quantity || ""}</td>
                    <td>${instance.purchase_return_amount || ""}</td>
                </tr>`
            )
            console.log(data)
        },
    })
})