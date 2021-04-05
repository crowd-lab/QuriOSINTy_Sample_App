$(document).ready(function() {

    // Set up the table
    $('#task_list_table').DataTable( {
        "pagingType": "full_numbers",
        "order": [[ 4, "desc" ]]
    } );
    
});