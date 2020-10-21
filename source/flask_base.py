from datetime import datetime

from flask import Flask, Blueprint, render_template, request, redirect, flash, session, json
import requests
from flask_forms import CreateAccount, ChangeLeaveAllowance, ChangePassword, LeaveRequest, ChangeUserRole, PublicHolidays
from flask_database_api import FlaskDatabaseApi
from flask import jsonify
import re

base = Blueprint("base", __name__)


# Main
# Session staffID,name,role
@base.route("/", methods=["GET", "POST"])
def index():
    # Use REST API.
    # response = requests.get("http://127.0.0.1:5000/")
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        # do authentication
        with FlaskDatabaseApi() as db:
            if (db.checkStaffUsername(username)):
                session['staffID'] = db.checkStaffUsername(username)
                if db.checkStaffPassword(session['staffID'], password):
                    nameRole = db.getNameRole(session['staffID'])
                    session['name'] = nameRole[0]
                    session['role'] = nameRole[1]
                    session['loggedIN'] = True
                    flash("Login was successful", "success")
                    if session['role'] == 'staff':
                        return redirect(request.url + "staff_profile")
                    if session['role'] == 'manager':
                        return redirect(request.url + "staff_by_manager")
                    if session['role'] == 'admin':
                        return redirect(request.url + "home")
                    else:
                        flash("Unauthorized error Invalid role : " + session['role'], "danger")
                        return render_template('unauthorized.html')
                else:
                    session['staffID'] = None
                    session['loggedIN'] = None
                    flash("Incorrect password, please try again!", "danger")
                    return redirect('/')

            else:
                flash("Incorrect username, please try again!", "danger")
                return redirect('/')
    return render_template("index.html")


@base.route("/logout")
def logout():
    session.pop('loggedIN', None)
    return redirect('/')


# Admin
@base.route("/home", methods=["GET", "POST"])
def home():
    if not session.get('loggedIN'):
        return redirect('/')

    return render_template("home.html")


@base.route("/list_staff_member", methods=["GET"])
def list_staff_member():
    if not session.get('loggedIN'):
        return redirect('/')

    with FlaskDatabaseApi() as db:
        response = {"data": db.getAllStaff()}
        return jsonify(response)


@base.route("/deactivate", methods=["POST"])
def deactivate():
    if not session.get('loggedIN'):
        return redirect('/')

    req = request.form
    staffID = req.get("userID")
    print(staffID)
    with FlaskDatabaseApi() as db:
        result = db.deactivateStaff(staffID)
        return jsonify(result)


@base.route("/activate", methods=["POST"])
def activate():
    if not session.get('loggedIN'):
        return redirect('/')

    req = request.form
    staffID = req.get("userID")
    print(staffID)
    with FlaskDatabaseApi() as db:
        result = db.activateStaff(staffID)
        return jsonify(result)


@base.route("/create_account", methods=["GET", "POST"])
def create_account():
    if not session.get('loggedIN'):
        return redirect('/')

    form = CreateAccount()
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        with FlaskDatabaseApi() as db:
            db.insertStaff(username, name, email, password, role)
            flash("The account has been successfully created.", "success")
            return redirect('/home')
    return render_template("create_account.html", form=form)


@base.route("/changeLeaveAllowance", methods=["GET", "POST"])
def change_leaveAllowance():
    if not session.get('loggedIN'):
        return redirect('/')

    form = ChangeLeaveAllowance()
    staffID = request.args.get('userID')
    staffName = request.args.get('name')
    leaveLimit = request.args.get('limit')
    if form.validate_on_submit():
        leave = form.limitLeaveAllowance.data
        userID = request.form.get('userID')
        with FlaskDatabaseApi() as db:
            db.updateLeaveAllowance(userID, leave)
            # print("{} updated.".format(leave))
            flash("The leave allowance has been successfully updated.", "success")
            return redirect('/home')
    return render_template("change_leaveAllowance.html", form=form,
                           data={"staffID": staffID, "staffName": staffName, "leaveLimit": leaveLimit})



# staff
@base.route("/staff_profile", methods=["GET", "POST"])
def staff_profile():
    if not session.get('loggedIN'):
        return redirect('/')
    name = session.get('name')
    role = session.get('role')
    staff_id = session.get('staffID')
    with FlaskDatabaseApi() as db:
        if db.getLeaveBalance(staff_id):
            leave_balance = db.getLeaveBalance(staff_id)
            return render_template("staff_profile.html",
                                   data={"name": name, "role": role, "leaveBalance": leave_balance})
        flash("Unable to fetch leave  balance [db server error]", "danger")
        return render_template("staff_profile.html",
                               data={"name": name, "role": role, "leaveBalance": 0})


@base.route("/leaveRequestList", methods=["GET"])
def leaveRequestList():
    if not session.get('loggedIN'):
        return redirect('/')

    with FlaskDatabaseApi() as db:
        response = {"data": db.getLeaveRequestHistory(session['staffID'])}
        print(response)
        return jsonify(response)


@base.route("/leave_request_history", methods=["GET", "POST"])
def leave_request_history():
    if not session.get('loggedIN'):
        return redirect('/')

    return render_template("leave_request.html")


@base.route("/cancelLR", methods=["POST"])
def cancelLR():
    if not session.get('loggedIN'):
        return redirect('/')

    req = request.form
    reqID = req.get("leaveRqID")
    print(reqID)
    with FlaskDatabaseApi() as db:
        result = db.cancelLeaveRequest(reqID)
        return jsonify(result)


@base.route("/leaveRequest", methods=["GET", "POST"])
def leave_request():
    if not session.get('loggedIN'):
        return redirect('/')
    form = LeaveRequest()
    if request.method == 'POST':
        date = form.leaveRequest.data
        user_id = session['staffID']
        dates = date.split(' - ')
        start_date = datetime.strptime(dates[0], '%m/%d/%Y')
        end_date = datetime.strptime(dates[1], '%m/%d/%Y')
        with FlaskDatabaseApi() as db:
            db.putLeaveRequest(user_id, start_date, end_date)
            flash("The leave request has submitted.", "success")
            return redirect('/staff_profile')
    return render_template("_leaveRequest.html", form=form)


@base.route("/setting", methods=["GET", "POST"])
def setting():
    if not session.get('loggedIN'):
        return redirect('/')

    form = ChangePassword()
    if form.validate_on_submit():
        old_password = form.pass_old.data
        new_password = form.pass_new.data
        with FlaskDatabaseApi() as db:
            if db.checkStaffPassword(session['staffID'], old_password) == True:
                db.changePassword(session['staffID'], new_password)
                flash("The password has been changed.", "success")
            else:
                flash("The password has not been matched!.", "danger")
        return redirect('/setting')

    return render_template("setting.html", form=form)


# *************************** Manager **************************************

@base.route("/list_staff_by_manager", methods=["GET"])
def list_staff_by_manager():
    if not session.get('loggedIN'):
        return redirect('/')

    with FlaskDatabaseApi() as db:
        staff_list = db.getStaffManaged(session['staffID'])
        response = {"data": []}
        if staff_list:
            response = {"data": staff_list}
        print(staff_list)
        return jsonify(response)


@base.route("/staff_by_manager", methods=["GET"])
def staff_by_manager():
    if not session.get('loggedIN'):
        return redirect('/')
    with FlaskDatabaseApi() as db:
        staff_list = db.getStaffManaged(session['staffID'])
        require_add_staff = False
        if staff_list is None:
            require_add_staff = True

        print(require_add_staff)
    return render_template('list_staff.html', require_add_staff=require_add_staff)


@base.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if not session.get('loggedIN'):
        return redirect('/')
    if request.method == 'POST':
        req = request.form
        user_id = session['staffID']
        staff_id = req.get("staffID")
        with FlaskDatabaseApi() as db:
            response = db.addStaff(user_id, staff_id)
            return jsonify(response)
    return render_template('add_staff.html')


@base.route("/list_available_staff", methods=["GET"])
def list_available_staff():
    if not session.get('loggedIN'):
        return redirect('/')
    with FlaskDatabaseApi() as db:
        # should show only available staff?
        all_staff = db.getAllStaff()

        response = {"data": db.getAllStaff()}
        return jsonify(response)

@base.route("/leaveRequestListStaff", methods=["GET"])
def leaveRequestListStaff():
    if not session.get('loggedIN'):
        return redirect('/')

    with FlaskDatabaseApi() as db:
        response = {"data": db.getPendingLeaveRequests(session['staffID'])}
        print(response)
        return jsonify(response)


@base.route("/leaveRequestStaff", methods=["GET", "POST"])
def leaveRequestStaff():
    if not session.get('loggedIN'):
        return redirect('')

    return render_template("leave_requestStaff.html")


@base.route("/approveLR", methods=["POST"])
def approveLR():
    if not session.get('loggedIN'):
        return redirect('/')

    req = request.form
    reqID = req.get("leaveRqID")
    print(reqID)
    with FlaskDatabaseApi() as db:
        result = db.updateLeaveRequestStatus(reqID, "Granted")
        return jsonify(result)


@base.route("/rejectLR", methods=["POST"])
def rejectLR():
    if not session.get('loggedIN'):
        return redirect('/')

    req = request.form
    reqID = req.get("leaveRqID")
    print(reqID)
    with FlaskDatabaseApi() as db:
        result = db.updateLeaveRequestStatus(reqID, "Rejected")
        return jsonify(result)


# change role of users by Admin
@base.route("/changeStaffRole", methods=["POST", "GET"])
def changeStaffRole():
    if not session.get('loggedIN'):
        return redirect('/')

    role = request.args.get('role')
    form = ChangeUserRole(role= role)
    staffID = request.args.get('userID')
    staffName = request.args.get('name')
    if form.validate_on_submit():
        role = form.role.data
        userID = request.form.get('userID')
        print(role)
        print(userID)
        with FlaskDatabaseApi() as db:
            db.changeRole(userID, role)
            flash("The role has been successfully updated.", "success")
            return redirect('/home')
    
    return render_template("change_role.html", form=form,data={"staffID": staffID, "staffName": staffName})

# view public holidays 
@base.route("/publicHolidayView", methods=["POST","GET"])
def publicHolidayView():
    if not session.get('loggedIN'):
        return redirect('/')

    return render_template("public_holidays.html")

@base.route("/publicHolidayList", methods=["GET"])
def publicHolidayList():
    if not session.get('loggedIN'):
        return redirect('/')

    with FlaskDatabaseApi() as db:
        response = {"data": db.getAllPublicHolidays(2020)}
        return jsonify(response)

# add public holidays
@base.route("/addPublicHoliday", methods=["GET", "POST"])
def addPublicHoliday():
    if not session.get('loggedIN'):
        return redirect('/')

    form = PublicHolidays()
    if form.validate_on_submit():
        holiday = form.holidayName.data
        start = form.startDate.data
        end = form.endDate.data
        with FlaskDatabaseApi() as db:
            db.insertPublicHolidays(holiday, start, end, 2020)
            flash("The public holidays have been successfully created.", "success")
            return redirect('/publicHolidayView')
            
    return render_template("_public_holidays_add.html", form=form)
    
    

