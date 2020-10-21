$(document).ready(function () {

    const tableRq = $('#leaveRequestList').DataTable({
        "ajax": "/leaveRequestList",
        "dataSrc": "",
        "columns": [
            {"data": 0},
            {"data": 3},
            {"data": 4},
            {
                "data": "Status",
                "render": function (data,type, row) {
                    let st="";
                    switch(row[5]) {
                        case 'Pending':
                            st = 'text-warning';
                            break;
                        case 'Granted':
                            st = 'text-success';
                            break;
                        case 'Rejected':
                            st = 'text-secondary';
                            break;
                        case 'Cancelled':
                            st = 'text-danger';
                            break;
                    }
                    return '<p class=' + st +'>'+ row [5]+'</p>';
                }
            
            },
            {
                "data": "Action",
                "render": function (data, type, row) {             
                    let button = ' <button class="btn btn-mini btn-danger btn-sm" id="leaveReq"> Cancel</button>';  
                    if (row[5] != 'Pending') {
                        button = '';
                    }
                    return button;   
                }
            }
        ]
    });


    $(document.body).on('click', '#leaveReq', function () {
        let data = tableRq.row($(this).parents('tr')).data();
        $.post('cancelLR', {leaveRqID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                tableRq.ajax.reload();
            } else {
                alert("Unsuccessful!");
            }
        });
    });


    $(document.body).on('click', '#showLeaveRequestModal', function () {
        // $('#putLeaveRequest').modal({show: true});

        $('.modal-body').load('leaveRequest', function () {
            $('#putLeaveRequest').modal({show: true});
            $('input[name="leaveRequest"]').daterangepicker({
                parentEl: $('#putLeaveRequest'),
                showDropdowns: true,
            }, function (start, end, label) {
            });
        });
    });


    // $('input[name="birthday"]').daterangepicker({parentEl: $('#putLeaveRequest'), showDropdowns: true,});
    $(document).on('submit', '#leaveRequest', function (e) {
        // console.log('submitted');
        // e.preventDefault();
        // $.post(url, data = $('#leaveRequest').serialize(), function (
        //     data) {
        //     if (data.status == 'ok') {
        //         $('#putLeaveRequest').modal('hide');
        //         location.reload();
        //     } else {
        //         var obj = JSON.parse(data);
        //         for (var key in obj) {
        //             if (obj.hasOwnProperty(key)) {
        //                 var value = obj[key];
        //             }
        //         }
        //         $('.form-group').addClass('has-error')
        //     }
        // })
    });


    const tableRqStf = $('#leaveRequestListStaff').DataTable({
        "ajax": "/leaveRequestListStaff",
        "dataSrc": "",
        "columns": [
            {"data": 0},
            {"data": 2},
            {"data": 3},
            {"data": 4},
            {
                "data": "Status",
                "render": function (data,type, row) {
                    let st="";
                    switch(row[5]) {
                        case 'Pending':
                            st = 'text-warning';
                            break;
                        case 'Granted':
                            st = 'text-success';
                            break;
                        case 'Rejected':
                            st = 'text-secondary';
                            break;
                        case 'Cancelled':
                            st = 'text-danger';
                            break;
                    }
                    return '<p class=' + st +'>'+ row [5]+'</p>';
                }
            
            },
            {
                "data": "Action",
                "render": function (data, type, row) {             
                    let button = ' <button class="btn btn-mini btn-success btn-sm" id="leaveReqApprove"> Approve</button>';  
                    button += ' <button class="btn btn-mini btn-danger btn-sm" id="leaveReqReject"> Reject</button>';
                    if (row[5] != 'Pending') {
                        button = '';
                    }
                    return button;   
                }
            }
        ]
    });


    $(document.body).on('click', '#leaveReqApprove', function () {
        let data = tableRqStf.row($(this).parents('tr')).data();
        $.post('approveLR', {leaveRqID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                tableRqStf.ajax.reload();
            } else {
                alert("Unsuccessful!");
            }
        });
    });

    $(document.body).on('click', '#leaveReqReject', function () {
        let data = tableRqStf.row($(this).parents('tr')).data();
        $.post('rejectLR', {leaveRqID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                tableRqStf.ajax.reload();
            } else {
                alert("Unsuccessful!");
            }
        });
    });


});
    

