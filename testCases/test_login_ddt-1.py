import time
import pytest
from selenium import webdriver
# now to access the action methods within loginPage.py file
from pageObjects.Locators import LoginPage
# =====================================
# below line is to get access to the utilities file
from utilities.readProperties import ReadConfig
# now importing the logger class to access it within this file
from utilities.customLogger import LogGen
from utilities import XLUtils


# web login details: server url + login credentials
class Test_DDT_login:
    # create variables for login
    # below valriables values are coming from utilities.ini file
    # which is further coming from readProperties.py file
    # now ReadConfig class can directly call the methods

    baseURL = ReadConfig.getURL()
    # now we're taking login details from below excel file
    path = ".//TestData/DataManager.xlsx"
    # therefore, we dont need below 2 lines of code

    # username = ReadConfig.getUsername()
    # password = ReadConfig.getPassword()

    # below method call is directly using the "logGen" class becoz its a static method
    # declaring a logger variable, becoz loggen() returns a logger in the logGen class

    logger = LogGen.loggen()

    # now, this logger variable will be used to send log messages
    # simple login test
    # def test_login(self):
    def test_login_ddt(self, setup):
        self.logger.info("******** Test+002_DDT_LoginTest*****")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)
        time.sleep(5)
        # ******** Changes For DDT *********
        # here we'll pass two parameters to get the row count
        # 1st is path of the excel file which is in PATH Variable
        # 2nd is excel file name, "sheet1" in LoginDataSheet
        self.rows = XLUtils.getRowCount(self.path, 'Sheet1')
        print("Number of rows in Excel: ", self.rows)
        # the results of the test
        # this will contain only Pass/Fail
        # to iterate all rows/values within the excel file
        # we started the range from 2, bcz, the header should not considered
        # within the Excel sheet data
        for r in range(2, self.rows+1):

            try:
                self.user = XLUtils.readData(self.path, 'Sheet1', r, 1)
                self.password = XLUtils.readData(self.path, 'Sheet1', r, 2)

                self.lp.setUserName(self.user)
                self.lp.setPassword(self.password)
                self.lp.clickLogin()
                time.sleep(10)
                # capture of the homepage once logged in
                # belo try is to check if the title is available
                actual_title = self.driver.title
                title_options = ["GENERIC Dashboard", "3DEXPERIENCE Platform", "PIC Generic"]

                if any(x in actual_title for x in title_options):
                    time.sleep(3)
                    self.lp.clickProfile()
                    time.sleep(2)
                    self.lp.clickLogout()
                    time.sleep(5)
                else:
                    self.logger.info("*** Title not found**")
            except Exception as e:
                self.logger.info("*** Logout Failed****")
                raise e


            # below check is to see if there is any FAILED test case within
            # the lst_Status variable, then this condition will be displayed

        self.logger.info("***** End of Login DDT Tests ****")
        self.logger.info("****** Completed Test_002_DDT_login ***")
