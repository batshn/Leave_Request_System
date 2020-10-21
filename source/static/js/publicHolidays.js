$(document).ready(function () {

    const tablePublicHD = $('#publicHolidayList').DataTable({
        "ajax": "/publicHolidayList",
        "dataSrc": "",
        "columns": [
            {"data": 1},
            {"data": 2},
            {"data": 3}
        ]
    }); 

});
    

