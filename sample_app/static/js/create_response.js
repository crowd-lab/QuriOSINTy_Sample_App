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

$(document).ready(function() {
    $('#img_url').change(function(){
        $('#previewImage').css({'max-width' : '500px' , 'max-height' : '500px'});
        $('#previewImage').attr("src", $('#img_url').val());

    });

    document.getElementById('create_response_form').onsubmit=function(e){
        e.preventDefault();
    };

    // Send form to the server
    $('#submit_btn').click(function() {
        var ans1 = $("#ans1").val();
        var ans2 = $("#ans2").val();
        var ans3 = $("#ans3").val();
        
        if(ans1.length == 0) {
                console.log("Fields not set.");
                return;
        }

        data = {
            "ans1": ans1,
            "ans2": ans2,
            "ans3": ans3
        };

        var task_id = window.location.href.split("/")[4];
        url = "/task/"+String(task_id)+"/response/add/";
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: url,
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: data,
            dataType: "json"
          }).done(function(response) {
            $("#submit_btn").prop("disabled",true);
            // window.location.replace("/task/"+String(task_id)+"/response/"+String(response)+"/");
          }).fail(function (error) {
            $('#submit_btn').prop("disabled",false);
              console.log(error);
          });

    });



});