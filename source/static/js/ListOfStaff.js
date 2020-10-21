$(document).ready(function () {


    const table = $('#staffMemberList').DataTable({
        "ajax": "/list_staff_member",
        "dataSrc": "",
        "columns": [
            {"data": 2},
            {"data": 3},
            {"data": 5},
            {"data": 7},
            {
                "data": "action",
                "render": function (data, type, full) {
                    console.log(full);
                    let button = '<button class="btn btn-mini btn-secondary btn-sm" id="showChangeRoleModal">Role</button>';
                    button += ' <button class="btn btn-mini btn-primary btn-sm" id="showChangeLeaveAllowanceModal">Leave Allowance</button>';
                    if (full[7] === 'Deactivated') {
                        //check if the account is activated
                        button += ' <button class="btn btn-mini btn-success btn-sm" id="activateStaff"> Activate</button>';
                    } else {
                        button += ' <button class="btn btn-mini btn-danger btn-sm" id="deactivateStaff" > Deactivate</button>';

                    }

                    
                    return button;
                }

            }
        ]
    });

    $(document.body).on('click', '#showChangeLeaveAllowanceModal', function () {
        let data = table.row($(this).parents('tr')).data();
        console.log(data);
        $('.modal-body').load('changeLeaveAllowance?userID=' + data[0] + '&name=' + data[2] + '&limit=' + data[7], function () {
            $('#changeLeaveAllowanceModal').modal({show: true});
        });
    });


    $(document.body).on('click', '#showChangeRoleModal', function () {
        let data = table.row($(this).parents('tr')).data();
        console.log(data);
        $('.modal-body').load('changeStaffRole?userID=' + data[0] + '&name=' + data[2] + '&role=' + data[5], function () {
            $('#changeRoleModal').modal({show: true});
        });
    });

    $(document.body).on('click', '#deactivateStaff', function () {
        let data = table.row($(this).parents('tr')).data();
        $.post('deactivate', {userID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                table.ajax.reload();
            } else {
                alert("db error")
            }
        });
    });

    $(document.body).on('click', '#activateStaff', function () {
        let data = table.row($(this).parents('tr')).data();
        $.post('activate', {userID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                table.ajax.reload();
            } else {
                alert("db error")
            }
        });
    });

    // manager function
    /**
     index 2 =  Name
     index 3 =  Email
     index 5 =  Role
     index 6 =  Balance
     index 7 =  Allowance
     **/
    const staffList = $('#availableStaffList').DataTable({
        "ajax": "/list_available_staff",
        "dataSrc": "",
        language: {
            emptyTable: "No staff found."
        },
        "columns": [
            {"data": 2},
            {"data": 3},
            {
                "data": "action",
                "render": function (data, type, full) {
                    return '<button class="btn btn-mini btn-primary" id="addStaff">Add Staff</button>';
                }

            }
        ]
    });

    const staffByManager = $('#staffListByManager').DataTable({
        "ajax": "/list_staff_by_manager",
        "dataSrc": "",
        "columns": [
            {"data": 2},
            {"data": 3},
            {"data": 5},
            {"data": 6},
            {"data": 7}
        ]
    });

    $(document.body).on('click', '#addStaff', function () {
        let data = staffList.row($(this).parents('tr')).data();
        $.post('add_staff', {staffID: data[0]}, function (result) {
            console.log(result);
            if (result) {
                table.ajax.reload();
            } else {
                alert("db error")
            }
        });
    });


});
