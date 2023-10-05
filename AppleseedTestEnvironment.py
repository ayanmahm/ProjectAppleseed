import unittest
import DatabaseManagement
import UserInterfaceEnv
import hashlib
import main
import ValidationProcess


class TestClass(unittest.TestCase):
    # test for details that exist
    def testUserSuccess(self):
        pw = hashlib.md5("".encode()).hexdigest()
        self.assertTrue(DatabaseManagement.testForExistence(table="users", username="ayanmahmood", password=pw), "A user with those details did not exist.")

    # test for details that do not exist
    def testUserFailure(self):
        self.assertFalse(DatabaseManagement.testForExistence(table="users", username="ayanmahmood", password="program"), "A user with those details exists.")

    # test for invalid validations
    def testValidationProcess(self):
        # test to see if the algorithm blocks invalid inputs
        print("Testing forbidden character detection")
        self.assertEqual(ValidationProcess.ValidateInput(Input='''£$apple"dkdk@!"£$$%^^^^&***'''), 1,
                         "There was a failure in the exception handler.")
        # Test to see if the algorithm blocks items that are too short.
        print("Testing forbidden length detection")
        self.assertEqual(ValidationProcess.ValidateInput(Input='''pw'''), 2, "There was a failure in the length handler.")

    def testSendFailure(self):
        print("Testing send mechanism")
        w = UserInterfaceEnv.sendClass(user="", rec="", title="", url="")
        self.assertFalse(w.upload())

    def testSendSuccess(self):
        w = UserInterfaceEnv.sendClass(user="user1", rec="user2", title="Test", url="ayanmahm.notion.site")
        self.assertTrue(w.upload())