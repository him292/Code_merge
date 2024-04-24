import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardTabs, iframes, placeholder_creation
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import ExcelUtils


class Test__Placeholder:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    path = "D://Git//test-automation//feature//Code_merge//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    logger = LogGen.loggen()

    def test_placeholder(self, setup):
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
        time.sleep(10)

        self.ph.click_PH_button()
        time.sleep(2)

        doctype = ExcelUtils.readData(self.path, 'Placeholder', 5, 1)
        number = ExcelUtils.readData(self.path, 'Placeholder', 2, 2)
        self.ph.ph_DocType(doctype, number)
        time.sleep(2)

        # this is commented becz I added the condition to add the serial only if docType = MDL or DRG

        # serial = ExcelUtils.readData(self.path, 'Placeholder', 2, 2)
        # self.ph.ph_serial(serial)
        # time.sleep(2)

        phTitle = ExcelUtils.readData(self.path, 'Placeholder', 2, 3)
        self.ph.ph_title(phTitle)
        time.sleep(2)

        region = ExcelUtils.readData(self.path, 'Placeholder', 2, 4)
        self.ph.ph_region(region)
        time.sleep(2)

        organisation = ExcelUtils.readData(self.path, 'Placeholder', 2, 5)
        self.ph.ph_organisation(organisation)
        time.sleep(2)

        discipline = ExcelUtils.readData(self.path, 'Placeholder', 2, 6)
        self.ph.ph_discipline(discipline)
        time.sleep(2)

        wo = ExcelUtils.readData(self.path, 'Placeholder', 2, 7)
        self.ph.ph_wo(wo)
        time.sleep(2)

        stage = ExcelUtils.readData(self.path, 'Placeholder', 2, 8)
        self.ph.ph_stage(stage)
        time.sleep(2)

        number = ExcelUtils.readData(self.path, 'Placeholder', 2, 9)
        # self.logger.info("doctypeCheck is " + str(doctype))
        if doctype == 'MDL - BIM Model' or doctype == 'DRG - Drawing':
            self.ph.ph_bookmark()
        else:
            if doctype != 'MDL - BIM Model' or doctype != 'DRG - Drawing':
                self.ph.ph_howMany(number)
                time.sleep(1)
                self.ph.ph_bookmark()
        time.sleep(2)

        self.ph.ph_createButton()
        time.sleep(20)

        self.ph.validate_ph_and_revision(phTitle)
        time.sleep(2)
