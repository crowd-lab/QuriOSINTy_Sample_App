$(document).ready(function() {

    $('#approve_response_btn').click(function() {
        var response_id = window.location.href.split("/")[6];
        url = "/response/"+String(response_id)+"/judge/0/";
        console.log(url);
        $.get(url, function() {
          })
            .done(function() { // checks for response code 2XX (200, etc.)
              location = location;
            })
            .fail(function() { // checks for response code 4XX (400, etc.)
              alert( "Error approving response." );
              location = location;
            })
    });
    
    $('#reject_response_btn').click(function() {
        var response_id = window.location.href.split("/")[6];
        url = "/response/"+String(response_id)+"/judge/1/";
        console.log(url);
        $.get(url, function() {
          })
            .done(function() { // checks for response code 2XX (200, etc.)
                location = location;
            })
            .fail(function() { // checks for response code 4XX (400, etc.)
              alert( "Error rejecting response." );
              location = location;
            })
    });

});