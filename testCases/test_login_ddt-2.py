import time
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.Locators import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import XLUtils

class Test_002_DDT_Login:
    path = ".//TestData//DataManager.xlsx"
    #get data from utility file to avoid hard coded values in test file
    baseURL = ReadConfig.getURL()
    #username = ReadConfig.getUsername()
    #password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    # Use self keyword to access Class
    def test_login_ddt(self,setup):
        self.logger.info("********** Test_002_DDT_Login ********")
        self.logger.info("********** Verifying login DDT test ********")
        self.driver = setup
        self.driver.get(self.baseURL)
    #create object of login class to access methods in it
        self.lp = LoginPage(self.driver)
        time.sleep(5)

        self.rows = XLUtils.getRowCount(self.path,"Sheet1")
        print("Number of row in excel",self.rows)

        lst_status=[]       #empty list variable to store status
        for r in range(2, self.rows+1):

            self.driver = setup
            self.driver.get(self.baseURL)
            # create object of login class to access methods in it
            self.lp = LoginPage(self.driver)
            time.sleep(5)

            self.username = XLUtils.readData(self.path,"Sheet1",r,1)
            self.password = XLUtils.readData(self.path,"Sheet1",r,2)
            self.exp = XLUtils.readData(self.path,"Sheet1",r,3)

            self.lp.setUserName(self.username)
            self.lp.setPassword(self.password)
            self.lp.clickLogin()
            time.sleep(10)

            act_title = self.driver.title
            print(act_title)
            exp_title = __contains__("GENERIC Dashboard")

            if act_title == exp_title:
                if self.exp == "Pass":
                    self.logger.info("*** Passed ***")
                    self.lp.clickProfile()
                    time.sleep(2)
                    self.lp.clickLogout()
                    time.sleep(10)
                    lst_status.append("Pass")
                elif self.exp == "Fail":
                    self.logger.info("*** Failed ***")
                    self.lp.clickProfile()
                    time.sleep(2)
                    self.lp.clickLogout()
                    time.sleep(10)
                    lst_status.append("Fail")

            elif act_title != exp_title:
                if self.exp == "Pass":
                    self.logger.info("*** Failed ***")
                    self.lp.clickProfile()
                    time.sleep(2)
                    self.lp.clickLogout()
                    time.sleep(10)
                    lst_status.append("Fail")
                elif self.exp == "Fail":
                    self.logger.info("*** Passed ***")
                    self.lp.clickProfile()
                    time.sleep(2)
                    self.lp.clickLogout()
                    time.sleep(10)
                    lst_status.append("Pass")
            self.driver.quit()
            self.driver.close()

        if "Fail" not in lst_status:
            self.logger.info("*** Login DDT test is passed.***")
            self.driver.close()
            assert True
        else:
            self.logger.info("*** Login DDT test is Failed.***")
            self.driver.close()
            assert False
        self.logger.info("*** End of Login DDT Test ***")
        self.logger.info("*** Test_002_DDT_Login test completed ***")
