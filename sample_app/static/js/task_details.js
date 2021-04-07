$(document).ready(function() {

    // Set up the table
    $('#task_response_table').DataTable( {
        "pagingType": "full_numbers",
        "order": [[ 4, "desc" ]]
    } );

    $('#close_task_btn').click(function() {
        var task_id = window.location.href.split("/")[4];
        url = "/task/"+String(task_id)+"/update/closed";
        console.log(url);

        $.get(url, function() {
          })
            .done(function() { // checks for response code 2XX (200, etc.)
            //   alert( "Task closed!" );
              location = location;
            })
            .fail(function() { // checks for response code 4XX (400, etc.)
              alert( "Error closing task." );
              location = location;
            })
    });

    $('#reopen_task_btn').click(function() {
        var task_id = window.location.href.split("/")[4];
        url = "/task/"+String(task_id)+"/update/open/";
        console.log(url);

        $.get(url, function() {
          })
            .done(function() { // checks for response code 2XX (200, etc.)
            //   alert( "Task reopened!" );
              location = location;
            })
            .fail(function() { // checks for response code 4XX (400, etc.)
              alert( "Error opening task." );
              location = location;
            })
    });
    
});