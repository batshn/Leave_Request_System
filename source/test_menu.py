from flask_database_api import FlaskDatabaseApi
import re

class Menu:
    def main(self):
        with FlaskDatabaseApi() as db:
            #db.dropLeaveRequestsTable()
            #db.dropStaffLeaveInfoTable()
            #db.dropStaffTable()
            
            db.createStaffMemberTable()
            db.createStaffLeaveInfoTable()
            db.createLeaveRequestsTable()
            db.createPublicHoliday()

            #db.insertStaff("test1","quazi","qz@gmail.com","123","staff")
            #db.insertStaff("test2","nithit","nithit@gmail.com","123","manager")
            #db.addStaff(2,1)
            #db.putLeaveRequest(1,"2020-10-14 00:00:00","2020-10-23 00:00:00","AnnualLeave")
            #db.updateLeaveRequestStatus(1,"Granted")

        self.runMenu()

    def runMenu(self):
        while(True):
            print()
            print("1. List Staff")
            print("2. Insert Staff")
            print("3. Password Validity Check")
            print("4. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listStaff()
            elif(selection == "2"):
                self.insertStaff()
            elif(selection == "3"):
                self.checkPasswordMenuHandler()
            elif(selection == "4"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def listStaff(self):
        print("--- Staff Members ---")
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Staff ID", "Username", "Name", "Email","Role","Leave Balance", "Leave Allowance", "Account Status"))
        with FlaskDatabaseApi() as db:
            for staff in db.getAllStaff():
                print(staff)
                # print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(staff[0], staff[1], staff[2], staff[3], staff[5], staff[6], staff[7], staff[8]))

    #no input validation done, just for initial testing phase
    def insertStaff(self):
        print("--- Insert Staff ---")
        username = input("Enter the staff username: ")
        name = input("Enter the staff name: ")
        email = input("Enter the staff email: ")
        role = input("Enter the staff role: ")
        password = input("Enter password: ")

        with FlaskDatabaseApi() as db:
            if(db.insertStaff(username,name,email,password,role)):
                print("{} inserted successfully.".format(name))
            else:
                print("{} failed to be inserted.".format(name))

    def checkPasswordValidity(self,password):
        s = ""

        #check missing uppercase letter
        if not any(x.isupper() for x in password):
            s += "Password must contain at least one uppercase letter\n"

        #check missing lower letter
        if not any(x.islower() for x in password):
            s += "Password must contain at least one lowercase letter\n"

        #check password length
        if not (len(password) >= 10):
            s += "Password must be at least 10 characters \n"
        
        #check missing digit
        if not any(x.isdigit() for x in password):
            s += "Password must contain at least one digit\n"
        
        #check for presence of special character
        sChar = re.compile('[!$*&+?<>()]')
        if not sChar.search(password):
            s += "Password must contain a special character out of '!, $, *, &, +, ?, <, >, (, )'"

        if len(s) > 0:
            print(s)
            #flash(s,"failure")
            return False
        else:
            return True 


    def checkPasswordMenuHandler(self):
        print("--- Password Validity Check ---")
        password = input("Enter password: ")
        
        if self.checkPasswordValidity(password):
            print("You have entered a valid password!")


if __name__ == "__main__":
    Menu().main()
