import unittest
from flask_database_api import FlaskDatabaseApi

class TestUser(unittest.TestCase):

    #unit test for creating account function (PBI1)
    def test_createAccount(self):

        #create test data to insert
        testUsername = "testuser1"
        testName = "Test User 1"
        testEmail = "testuser1@hotmail.com"
        testPassword = "helloworld"
        testRole = "Admin"
        staffID = None
        staff = None
        
        #insertion happens here
        with FlaskDatabaseApi() as db:
            self.assertTrue(db.insertStaff(testUsername,testName,testEmail,testPassword,testRole))
            staffID = db.checkStaffUsername(testUsername)
            
            #get the entire row for the staff just inserted
            staff = db.getStaff(staffID)

        #map each column of inserted data to relevant variables
        retrievedUsername = staff[1]
        retrievedName = staff[2]
        retrievedEmail = staff[3]
        retrievedPassword = staff[4]
        retrievedRole = staff[5]

        #do enough tests to make sure retrieved data matches test data 
        #created before insertion
        self.assertEqual(testUsername,retrievedUsername)
        self.assertEqual(testName,retrievedName)
        self.assertEqual(testEmail,retrievedEmail)
        self.assertNotEqual("12345678",retrievedPassword)
        self.assertNotEqual("Staff",retrievedRole)

        #delete the staff entry just created at the end of the test
        with FlaskDatabaseApi() as db:
            db.deleteStaff(staffID)

    #unit test for display all staff member list function (PBI3)
    def test_listAllStaff(self):
        oldStaffList = []
        newStaffList = []
        oldListLength = None 
        newListLength = None
        staffID1 = None 
        staffID2 = None
        with FlaskDatabaseApi() as db:
            #get list of all staff before inserting two staff members into it
            oldStaffList = db.getAllStaff()
            oldListLength = len(oldStaffList)
            
            self.assertTrue(db.insertStaff("testuser2","Test User 2","testuser2@hotmail.com","123456789","Staff"))
            self.assertTrue(db.insertStaff("testuser3","Test User 3","testuser3@hotmail.com","password","Manager"))
            
            staffID1 = db.checkStaffUsername("testuser2")
            staffID2 = db.checkStaffUsername("testuser3")
            
            #get list after for comparison
            newStaffList = db.getAllStaff()
            newListLength = len(newStaffList)

        #check if the list length increased by 2 and whether the last
        #two items on the new list is equal to the inserted values
        self.assertEqual(newListLength, oldListLength + 2)
        self.assertEqual(newStaffList[-2][1], "testuser2")
        self.assertEqual(newStaffList[-1][1], "testuser3")

        #delete the user created after test is over
        with FlaskDatabaseApi() as db:
            db.deleteStaff(staffID1)
            db.deleteStaff(staffID2)

    #unit test for deactivating staff member (PBI4)
    def test_deactivateStaffAccount(self):
        staffID = None
        oldStatus = None
        newStatus = None
        with FlaskDatabaseApi() as db:
            #insert a staff member and store initial account status
            self.assertTrue(db.insertStaff("testuser4","Test User 4","testuser4@hotmail.com","qwerty","Admin"))
            staffID = db.checkStaffUsername("testuser4")
            oldStatus = db.checkAccountStatus(staffID)

            #call the deactivate function and store new status
            db.deactivateStaff(staffID)
            newStatus = db.checkAccountStatus(staffID)

        #assert if status changes after calling deactivate staff function
        self.assertEqual(oldStatus,"Active")
        self.assertEqual(newStatus,"Deactivated")

        #delete the staff entry just created at the end of the test
        with FlaskDatabaseApi() as db:
            db.deleteStaff(staffID)


    #unit test for updating leave allowance of a staff member (PBI5)
    def test_updateLeaveAllowance(self):
        staffID = None
        oldAllowance = None
        newAllowance = None
        with FlaskDatabaseApi() as db:
            #insert a staff member and store initial leave allowance
            self.assertTrue(db.insertStaff("testuser5","Test User 5","testuser5@hotmail.com","zxcvbnm","Manager"))
            staffID = db.checkStaffUsername("testuser5")
            oldAllowance = db.getLeaveAllowance(staffID)

            #call the update leave allowance function and store new 
            #leave allowance
            db.updateLeaveAllowance(staffID,24)
            newAllowance = db.getLeaveAllowance(staffID)

        #assert if leave allowance after calling update leave allowance function
        self.assertEqual(oldAllowance,15) #leave allowance is 15 by default
        self.assertEqual(newAllowance,24)

        #delete the staff entry just created at the end of the test
        with FlaskDatabaseApi() as db:
            db.deleteStaff(staffID)


if __name__ == '__main__':
    unittest.main()