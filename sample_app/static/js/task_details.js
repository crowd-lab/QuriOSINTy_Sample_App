$(document).ready(function() {

    // Set up the table
    $('#task_response_table').DataTable( {
        "pagingType": "full_numbers",
        "order": [[ 4, "desc" ]]
    } );
    
});