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

    document.getElementById('create_task_form').onsubmit=function(e){
        e.preventDefault();
    };

    // Send form to the server
    $('#submit_btn').click(function() {
    
        var task_name = $('#task_name').val();
        var img_url = $('#img_url').val();
        // var evidence_list = JSON.stringify(Object.keys(evidence));

        var q1 = $("#q1").val();
        var q2 = $("#q2").val();
        var q3 = $("#q3").val();
        
        var num_responses = $("#num_responses").val();

        if(task_name.length == 0 || 
            img_url.length == 0 ||
            q1.length == 0 ||
            num_responses == 0) {
                console.log("Fields not set.");
                return;
        }

        data = {
            "task_name": task_name,
            "img_url": img_url,
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "num_responses": num_responses
        };

        url = "/task/new/add";
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: url,
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: data,
            dataType: "json"
          }).done(function(response) {
            $("#submit_btn").prop("disabled",true);
            window.location.replace("/task/"+String(response)+"/");
          }).fail(function (error) {
            $('#submit_btn').prop("disabled",false);
              console.log(error);
          });

    });



});