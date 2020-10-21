#install below module using "pip install PyMySQL"
#for more visit https://pypi.org/project/PyMySQL/
import pymysql
import datetime

class FlaskDatabaseApi:

    HOST = "35.189.29.183"
    USER = "root"
    PASSWORD = "sepm-g5"
    DATABASE = "Leave_Request_System"

    def __init__(self, connection = None):
        if(connection == None):
            connection = pymysql.connect(FlaskDatabaseApi.HOST, FlaskDatabaseApi.USER,
                FlaskDatabaseApi.PASSWORD, FlaskDatabaseApi.DATABASE)
        self.connection = connection
        
    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    #create table with staff member information
    def createStaffMemberTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists StaffMembers (
                    StaffID int not null auto_increment,
                    Username text not null,
                    Name text not null,
                    Email text not null,
                    Password text not null,
                    Role enum('admin','staff','manager') not null,
                    Manager text null,
                    AccountStatus enum('Active','Deactivated') not null,
                    constraint PK_Staff primary key (StaffID)
                )""")
        self.connection.commit()

    #create table with staff leave balance information
    def createStaffLeaveInfoTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists StaffLeaveInfo (
                    LeaveBalanceInfoID int not null auto_increment,
                    StaffID int not null,
                    Name text not null,
                    AnnualLeaveBalance int not null,
                    AnnualLeaveAllowance int not null,
                    CarersLeaveBalance int not null,
                    CarersLeaveAllowance int not null,
                    SickLeaveWithCertificateBalance int not null,
                    SickLeaveWithCertificateAllowance int not null,
                    SickLeaveWithoutCertificateBalance int not null,
                    SickLeaveWithoutCertificateAllowance int not null,
                    ParentalLeaveBalance int not null,
                    ParentalLeaveAllowance int not null,
                    primary key (LeaveBalanceInfoID),
                    constraint FK_StaffLeaveBalanceInfo foreign key (StaffID)
                    references StaffMembers(StaffID)
                )""")
        self.connection.commit()

    #create table with leave request information for each staff member
    def createLeaveRequestsTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists LeaveRequests (
                    LeaveRequestID int not null auto_increment,
                    StaffID int not null,
                    Name text not null,
                    LeaveType enum('AnnualLeave','CarersLeave','BloodDonor','SickLeaveWithCertificate','SickLeaveWithoutCertificate','ParentalLeave','UnpaidLeave') not null,
                    StartDate text not null,
                    EndDate text not null,
                    Status enum('Pending','Granted','Rejected','Cancelled') not null,
                    primary key (LeaveRequestID),
                    constraint FK_LeaveRequest foreign key (StaffID)
                    references StaffMembers(StaffID)
                )""")
        self.connection.commit()

    #create table with public holiday information
    def createPublicHoliday(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists PublicHolidays (
                    HdID int not null auto_increment,
                    HolidayName text not null,
                    StartDate text not null,
                    EndDate text not null,
                    HdYear int not null,
                    constraint PK_Holidays primary key (HdID)
                )""")
        self.connection.commit()

    #drop the staffmembers table
    def dropStaffTable(self):
        with self.connection.cursor() as cursor: 
            cursor.execute("DROP TABLE IF EXISTS StaffMembers")
        self.connection.commit()

    #drop the staffleaveinfo table
    def dropStaffLeaveInfoTable(self):
        with self.connection.cursor() as cursor: 
            cursor.execute("DROP TABLE IF EXISTS StaffLeaveInfo")
        self.connection.commit()
    
    #drop the leaverequests table
    def dropLeaveRequestsTable(self):
        with self.connection.cursor() as cursor: 
            cursor.execute("DROP TABLE IF EXISTS LeaveRequests")
        self.connection.commit()
    
     #drop the publicholiday table
    def dropPublicHoliday(self):
        with self.connection.cursor() as cursor: 
            cursor.execute("DROP TABLE IF EXISTS PublicHolidays")
        self.connection.commit()

    #fetch all data from staffmembers table
    def getAllStaff(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from StaffMembers")
            return cursor.fetchall()
    
    #insert staff info into the database
    def insertStaff(self,username,name,email,password,role):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into StaffMembers (Username,Name,Email,Password,Role,AccountStatus) values (%s,%s,%s,%s,%s,%s)", (username,name,email,password,role,"Active"))
            self.connection.commit()
            if cursor.rowcount == 1:
                staffID = self.checkStaffUsername(username)
                name = self.getNameRole(staffID)[0]
                self.setStaffLeaveInfo(staffID,name)
            return cursor.rowcount == 1

    #set initial staff leave balance and allowance info
    def setStaffLeaveInfo(self,staffID,name):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into StaffLeaveInfo (StaffID,Name,AnnualLeaveBalance,AnnualLeaveAllowance,CarersLeaveBalance,CarersLeaveAllowance,SickLeaveWithCertificateBalance,SickLeaveWithCertificateAllowance,SickLeaveWithoutCertificateBalance,SickLeaveWithoutCertificateAllowance,ParentalLeaveBalance,ParentalLeaveAllowance) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (staffID,name,20,20,15,15,30,30,7,7,168,168))
            self.connection.commit()
            return cursor.rowcount == 1

    #get all information of a staff member
    def getStaff(self,staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from StaffMembers where StaffID=%s limit 1",(staffID,))
            return cursor.fetchone()

    #delete all information of a staff member
    def deleteStaff(self,staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from StaffMembers where StaffID=%s",(staffID,))
        self.connection.commit()

    #check staff username and return the staffID if exists
    def checkStaffUsername(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("select StaffID from StaffMembers where Username = %s limit 1",(username,))
            staff = cursor.fetchone()
            if staff:
                return staff[0]
            else:
                return None
    
    #check if inputted password matches the password in database
    def checkStaffPassword(self, staffID, password):
        with self.connection.cursor() as cursor:
            cursor.execute("select Password from StaffMembers where StaffID = %s limit 1",(staffID,))
            dbPassword = cursor.fetchone()
            if dbPassword:
                if dbPassword[0] == password:
                    return True
                else:
                    return False
            else:
                return False

    #change password (assume password has been checked)
    def changePassword(self,staffID,password):
        with self.connection.cursor() as cursor:
            cursor.execute("update StaffMembers set Password=%s where StaffID=%s",(password,staffID))
        self.connection.commit()
        return cursor.rowcount == 1

    #deactivate a staff member
    def deactivateStaff(self, staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("update StaffMembers set AccountStatus=%s where StaffID=%s",("Deactivated",staffID))
        self.connection.commit()
        return cursor.rowcount == 1

    #activate a staff member
    def activateStaff(self, staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("update StaffMembers set AccountStatus=%s where StaffID=%s",("Active",staffID))
        self.connection.commit()
        return cursor.rowcount == 1

    #get account status of a staff member
    def checkAccountStatus(self, staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("select AccountStatus from StaffMembers where StaffID = %s limit 1",(staffID,))
            accountStatus = cursor.fetchone()
            if accountStatus:
                return accountStatus[0]
            else:
                return None

    #update a specific leave allowance of a staff (newAllowance = number to 
    # increase allowance by)
    def updateLeaveAllowance(self, staffID, leaveType, newAllowance):
        leaveAllowance = ""
        leaveBalance = ""
        if leaveType == "AnnualLeave":
            leaveAllowance = "AnnualLeaveAllowance"
            leaveBalance = "AnnualLeaveBalance"
        elif leaveType == "CarersLeave":
            leaveAllowance = "CarersLeaveAllowance"
            leaveBalance = "CarersLeaveBalance"
        elif leaveType == "SickLeaveWithCertificate":
            leaveAllowance = "SickLeaveWithCertificateAllowance"
            leaveBalance = "SickLeaveWithCertificateBalance"
        elif leaveType == "SickLeaveWithoutCertificate":
            leaveAllowance = "SickLeaveWithoutCertificateAllowance"
            leaveBalance = "SickLeaveWithoutCertificateBalance"
        elif leaveType == "ParentalLeave":
            leaveAllowance = "ParentalLeaveAllowance"
            leaveBalance = "ParentalLeaveBalance"

        with self.connection.cursor() as cursor:
            sql = "update StaffLeaveInfo set {}={}+{},{}={}-{} where StaffID=%s".format(leaveAllowance,leaveAllowance,newAllowance,leaveBalance,leaveBalance,newAllowance)
            cursor.execute(sql,(staffID,))
        self.connection.commit()
        return cursor.rowcount == 1

    #get leave allowance of a staff member
    def getLeaveAllowance(self, leaveType, staffID):
        if leaveType == "AnnualLeave":
            leave = "AnnualLeaveAllowance"
        elif leaveType == "CarersLeave":
            leave = "CarersLeaveAllowance"
        elif leaveType == "SickLeaveWithCertificate":
            leave = "SickLeaveWithCertificateAllowance"
        elif leaveType == "SickLeaveWithoutCertificate":
            leave = "SickLeaveWithoutCertificateAllowance"
        elif leaveType == "ParentalLeave":
            leave = "ParentalLeaveAllowance"

        with self.connection.cursor() as cursor:
            cursor.execute("select %s from StaffLeaveInfo where StaffID = %s limit 1",(leave,staffID,))
            leaveAllowance = cursor.fetchone()
            if leaveAllowance:
                return leaveAllowance[0]
            else:
                return []

    #check role
    def checkRole(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("select Role from StaffMembers where Username = %s limit 1",(username,))
            role = cursor.fetchone()
            if role:
                return role[0]
            else:
                return None
    
    #change role (assume role has been checked)
    def changeRole(self,staffID,role):
        with self.connection.cursor() as cursor:
            cursor.execute("update StaffMembers set Role=%s where StaffID=%s",(role,staffID))
        self.connection.commit()
        return cursor.rowcount == 1

    #get name & role
    def getNameRole(self, staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("select Name,Role from StaffMembers where StaffID = %s limit 1",(staffID,))
            nameRole = cursor.fetchone()
            if nameRole:
                return nameRole
            else:
                return None

    #get leave balance of an employee
    def getLeaveBalance(self, staffID):
        if leaveType == "AnnualLeave":
            leaveBalance = "AnnualLeaveBalance"
        elif leaveType == "CarersLeave":
            leaveBalance = "CarersLeaveBalance"
        elif leaveType == "SickLeaveWithCertificate":
            leaveBalance = "SickLeaveWithCertificateBalance"
        elif leaveType == "SickLeaveWithoutCertificate":
            leaveBalance = "SickLeaveWithoutCertificateBalance"
        elif leaveType == "ParentalLeave":
            leaveBalance = "ParentalLeaveBalance"

        with self.connection.cursor() as cursor:
            cursor.execute("select %s from StaffLeaveInfo where StaffID = %s limit 1",(leaveBalance,staffID))
            leaveBalance = cursor.fetchone()
            if leaveBalance:
                return leaveBalance[0]
            else:
                return None

    #insert leave request information for a staff member into the database
    def putLeaveRequest(self,staffID,startDate,endDate,leaveType):
        print(staffID)
        name = self.getNameRole(staffID)[0]
        with self.connection.cursor() as cursor:
            cursor.execute("insert into LeaveRequests (StaffID,Name,LeaveType,StartDate,EndDate,Status) values (%s,%s,%s,%s,%s,%s)",(staffID,name,leaveType,startDate,endDate,"Pending"))
            self.connection.commit()
            return cursor.rowcount == 1

    #cancel a pending leave request
    def cancelLeaveRequest(self,leaveRequestID):
        with self.connection.cursor() as cursor:
            cursor.execute("update LeaveRequests set Status=%s where LeaveRequestID=%s",("Cancelled",leaveRequestID))
        self.connection.commit()
        return cursor.rowcount == 1

    #get leave request history of a staff member
    def getLeaveRequestHistory(self,staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from LeaveRequests where StaffID = %s",(staffID,))
            history = cursor.fetchall()
            if history:
                return history
            else: 
                return None

    #add staff to put under a manager
    def addStaff(self,managerID,staffID):
        with self.connection.cursor() as cursor:
            cursor.execute("update StaffMembers set Manager=%s where StaffID=%s",(managerID,staffID))
        self.connection.commit()
        return cursor.rowcount == 1

    #cancel a pending leave request
    def cancelLeaveRequest(self,leaveRequestID):
        with self.connection.cursor() as cursor:
            cursor.execute("update LeaveRequests set Status=%s where LeaveRequestID=%s",("Cancelled",leaveRequestID))
        self.connection.commit()
        return cursor.rowcount == 1

    #get list of staff members who are not managed by anyone yet
    def getAvailableStaff(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from StaffMembers where Role = %s and Manager is NULL",("staff",))
            availableStaff = cursor.fetchall()
            if availableStaff:
                return availableStaff
            else: 
                return None

    #get list of staff managed by a manager
    def getStaffManaged(self,managerID):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from StaffMembers where Manager = %s",(managerID,))
            staffManaged = cursor.fetchall()
            if staffManaged:
                return staffManaged
            else:
                return []

    #get list of pending staff leave requests
    def getPendingLeaveRequests(self,managerID):
        staffList = self.getStaffManaged(managerID)
        staffIDs = [staff[0] for staff in staffList]
        pendingList = []
        finalList = []
        with self.connection.cursor() as cursor:
            cursor.execute("select * from LeaveRequests where Status = %s order by LeaveRequestID desc",("Pending",))
            pendingList = cursor.fetchall() 

        for row in pendingList:
            if row[1] in staffIDs:
                finalList.append(row)

        if finalList:
            return finalList
        else:
            return None

    #approve/reject of pending leave request (status must be "Granted" or "Rejected")
    #if granted this function calls the update leave balance function using optional
    #leave balance parameter
    def updateLeaveRequestStatus(self,leaveRequestID,status):
        with self.connection.cursor() as cursor:
            cursor.execute("update LeaveRequests set Status=%s where LeaveRequestID=%s",(status,leaveRequestID))
        self.connection.commit()
        if (status == "Granted"):
            self.updateLeaveBalance(leaveRequestID)
        return cursor.rowcount == 1

    #update leave balance function for when leave request is granted for a staff
    def updateLeaveBalance(self,leaveRequestID):
        with self.connection.cursor() as cursor:
            cursor.execute("select StaffID,StartDate,EndDate,LeaveType from LeaveRequests where LeaveRequestID = %s limit 1",(leaveRequestID,))
            result = cursor.fetchone()
            staffID = result[0]
            startDate = result[1]
            endDate = result[2]
            leaveType = result[3]
            days = self.workdays(startDate,endDate)

            #need to add adjustment for public holiday here

            if leaveType == "AnnualLeave":
                leaveBalance = "AnnualLeaveBalance"
            elif leaveType == "CarersLeave":
                leaveBalance = "CarersLeaveBalance"
            elif leaveType == "SickLeaveWithCertificate":
                leaveBalance = "SickLeaveWithCertificateBalance"
            elif leaveType == "SickLeaveWithoutCertificate":
                leaveBalance = "SickLeaveWithoutCertificateBalance"
            elif leaveType == "ParentalLeave":
                leaveBalance = "ParentalLeaveBalance"
            sql = "update StaffLeaveInfo set {}={}-{} where StaffID=%s".format(leaveBalance,leaveBalance,days)    
            cursor.execute(sql,(staffID,))
        self.connection.commit()
        return cursor.rowcount == 1

    #function that returns number of workdays between two date ranges
    #dates should be in (YYYY-mm-DD HH:MM:SS)    
    def workdays(self,start,end):
        try:
            s = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
            e = datetime.datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
            weekends = (6,7)
            days = 0
            while s.date() <= e.date():
                if s.isoweekday() not in weekends:
                    days += 1
                s += datetime.timedelta(days=1)
            return days
        except:
            return 0

    
     #insert public holidays into the database
    def insertPublicHolidays(self,hDay,StDate,EndDate,HdYear):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into PublicHolidays (HolidayName,StartDate,EndDate,HdYear) values (%s,%s,%s,%s)", (hDay,StDate,EndDate,HdYear))
            self.connection.commit()
            return cursor.rowcount == 1

    
    #get public holidays
    def getAllPublicHolidays(self,hdYear):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from PublicHolidays where HdYear = %s", (hdYear))
            holidays = cursor.fetchall()
            if holidays:
                return holidays
            else: 
                return []
