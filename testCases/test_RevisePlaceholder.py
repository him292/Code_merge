import time
import pytest
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsPlaceholder import placeholder_creation
from pageObjects.LocatorsDashboard import DashboardAndTabs
from pageObjects.LocatorsLoginPage import LoginPage
from pageObjects.LocatorsTransmittal import iframes
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_015_Revise_Placeholder:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    # path = ".//TestData//DataManager.xlsx"

    # logger = LogGen.loggen()

    def test_revise_placeholder(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        logger_setup.logger.info("*** Starting the Placeholder revise test ***")
        logger_setup.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        logger_setup.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        time.sleep(5)

        self.ph = placeholder_creation(self.driver)
        time.sleep(5)

        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.iframe.navigate_to_tab_registered_document()
        logger_setup.logger.info("*** Clicked on Registered Documents tab***")
        time.sleep(6)

        phTitle = XLUtils.readData(self.path, 'Placeholder', 2, 3)
        self.ph.select_click_ph_to_revise(phTitle)
        logger_setup.logger.info("*** PH " + phTitle + " is selected to revise ***")
        time.sleep(5)

        self.org_file_path = XLUtils.readData(self.path, "Placeholder", 2, 12)
        self.ph.ph_select_file(self.org_file_path, self.path)
        time.sleep(5)

        status = XLUtils.readData(self.path, 'Placeholder', 2, 13)
        self.ph.ph_Status(status)
        time.sleep(2)

        self.ph.ph_bookmark()
        time.sleep(2)

        self.ph.ph_reviseButton()
        logger_setup.logger.info("*** PH is successfully revised ***")
        time.sleep(20)

        phName = XLUtils.readData(self.path, 'Placeholder', 3, 12)
        self.ph.validate_revised_ph(phName)
        logger_setup.logger.info("*** PH " + phName + " is successfully validated ***")
        logger_setup.logger.info("*** End of Revise PH test case ***")
        time.sleep(2)
