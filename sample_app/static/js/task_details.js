$(document).ready(function() {

    // Set up the table
    $('#task_response_table').DataTable( {
        "pagingType": "full_numbers",
        "order": [[ 4, "desc" ]]
    } );

    $('#close-task-btn').click(function() {
        var task_id = window.location.href.split("/")[4];
        url = "/task/"+String(task_id)+"/close/";
        console.log(url);

        $.get(url, function() {
          })
            .done(function() { // checks for response code 2XX (200, etc.)
              alert( "Task closed!" );
            })
            .fail(function() { // checks for response code 4XX (400, etc.)
              alert( "Error closing task." );
            })
           

    });
    
});