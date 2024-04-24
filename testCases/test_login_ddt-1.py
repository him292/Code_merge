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

        #lst_status=[]       #empty list variable to store status
        for r in range(2, self.rows+1):
            try:
                self.username = XLUtils.readData(self.path,"Sheet1",r,1)
                self.password = XLUtils.readData(self.path,"Sheet1",r,2)

                self.lp.setUserName(self.username)
                self.lp.setPassword(self.password)
                self.lp.clickLogin()
                time.sleep(10)

                act_title = self.driver.title

                if act_title.__contains__("GENERIC Dashboard"):
                    self.driver.save_screenshot("D:\\Git//test-automation\\3DX_pythonProject\\Screenshots\\loginTest_screenshots\\" + self.username +".png")
                    self.logger.info("*** Login is passed by user - " + self.username)
                    self.logger.info(act_title)
                    self.lp.clickProfile()
                    time.sleep(5)
                    self.lp.clickLogout()
                    time.sleep(10)

                else:
                    self.logger.info("*** Login is Failed by user - " + self.username)
                    self.driver.save_screenshot(
                        "D:\\Git//test-automation\\3DX_pythonProject\\Screenshots\\loginTest_screenshots\\Failed\\" + self.username + ".png")
                    self.logger.info(act_title)
                    time.sleep(5)
            except Exception as e:
                self.logger.info("*** Test is Failed ***")
                raise e


        self.logger.info("*** End of Login DDT Test ***")
        self.logger.info("*** Test_002_DDT_Login test completed ***")
