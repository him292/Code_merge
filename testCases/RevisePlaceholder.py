import time
import pytest

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardTabs, iframes, placeholder_creation
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import ExcelUtils


@pytest.mark.placeholder
class Test__Revise_Placeholder:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    path = "D://My Projects//Selenium//TestFramework//TestData//LoginDataSheet.xlsx"

    logger = LogGen.loggen()

    def test_revise_placeholder(self, setup):
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.lp = LoginPage(self.driver)

        self.lp.setUsername(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)
        dashboard = "GENERIC Dashboard"

        self.dt = DashboardTabs(self.driver)
        time.sleep(5)

        self.ph = placeholder_creation(self.driver)
        time.sleep(5)

        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.iframe.navigate_to_tab_registered_document()
        self.logger.info("** Clicked on Registered Documents tab **")
        time.sleep(6)

        phTitle = ExcelUtils.readData(self.path, 'Placeholder', 2, 3)
        self.ph.select_click_ph_to_revise(phTitle)
        time.sleep(5)

        self.org_file_path = ExcelUtils.readData(self.path, "Placeholder", 2, 12)
        self.ph.ph_select_file(self.org_file_path)
        time.sleep(5)

        status = ExcelUtils.readData(self.path, 'Placeholder', 2, 13)
        self.ph.ph_Status(status)
        time.sleep(2)

        self.ph.ph_bookmark()
        time.sleep(2)

        self.ph.ph_reviseButton()
        time.sleep(20)

        phName = ExcelUtils.readData(self.path, 'Placeholder', 3, 12)
        self.ph.validate_revised_ph(phName)
        time.sleep(2)
