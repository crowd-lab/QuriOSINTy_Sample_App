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
    
        var task_id = $('#task_id').val();

        var q1 = $("#q1").val();
        var q2 = $("#q2").val();
        var q3 = $("#q3").val();
        
        if(q1.length == 0) {
                console.log("Fields not set.");
                return;
        }

        data = {
            "task_id": task_name,
            "q1": q1,
            "q2": q2,
            "q3": q3
        };

        url = "/response/new/add";
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: url,
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: data,
            dataType: "json"
          }).done(function(response) {
            $("#submit_btn").prop("disabled",true);
            window.location.replace("/task/"+String(task_id)+"/response/"+String(response)+"/");
          }).fail(function (error) {
            $('#submit_btn').prop("disabled",false);
              console.log(error);
          });

    });



});