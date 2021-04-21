function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
  function(m,key,value) {
    vars[key] = value;
  });
  return vars;
}

$(document).ready(function() {

    $('#approve_response_btn').click(function() {
        var response_id = getUrlVars()["response"];
        var auth_token = getUrlVars()["token"];
        url = "/response/"+String(response_id)+"/judge/0/"+String(auth_token)+"/";
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
        var response_id = getUrlVars()["response"];
        var auth_token = getUrlVars()["token"];
        url = "/response/"+String(response_id)+"/judge/1/"+String(auth_token)+"/";
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