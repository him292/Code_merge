import time
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsPlaceholder import placeholder_creation
from pageObjects.LocatorsDashboard import DashboardAndTabs
from pageObjects.LocatorsLoginPage import LoginPage
from pageObjects.LocatorsTransmittal import iframes
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_014_Placeholder:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    # path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    # logger = LogGen.loggen()

    def test_placeholder(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        logger_setup.logger.info("*** Starting Placeholder creation test ***")
        logger_setup.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        logger_setup.logger.info("*** User " + self.username + " successfully logged in ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        time.sleep(5)

        self.ph = placeholder_creation(self.driver)
        time.sleep(5)

        self.dt.clickdocumentmgtab()
        logger_setup.logger.info("*** Clicked on Document management tab ***")
        time.sleep(5)
        self.iframe.navigate_to_tab_registered_document()
        logger_setup.logger.info("*** Navigated on Registered Documents tab ***")
        time.sleep(10)

        self.ph.click_PH_button()
        logger_setup.logger.info("*** Clicked on create PH command ***")
        time.sleep(2)

        doctype = XLUtils.readData(self.path, 'Placeholder', 5, 1)
        number = XLUtils.readData(self.path, 'Placeholder', 2, 2)
        self.ph.ph_DocType(doctype, number)
        time.sleep(2)

        # this is commented becz I added the condition to add the serial only if docType = MDL or DRG

        # serial = ExcelUtils.readData(self.path, 'Placeholder', 2, 2)
        # self.ph.ph_serial(serial)
        # time.sleep(2)

        phTitle = XLUtils.readData(self.path, 'Placeholder', 2, 3)
        self.ph.ph_title(phTitle)
        time.sleep(2)

        region = XLUtils.readData(self.path, 'Placeholder', 2, 4)
        self.ph.ph_region(region)
        time.sleep(2)

        organisation = XLUtils.readData(self.path, 'Placeholder', 2, 5)
        self.ph.ph_organisation(organisation)
        time.sleep(2)

        discipline = XLUtils.readData(self.path, 'Placeholder', 2, 6)
        self.ph.ph_discipline(discipline)
        time.sleep(2)

        wo = XLUtils.readData(self.path, 'Placeholder', 2, 7)
        self.ph.ph_wo(wo)
        time.sleep(2)

        stage = XLUtils.readData(self.path, 'Placeholder', 2, 8)
        self.ph.ph_stage(stage)
        time.sleep(2)

        number = XLUtils.readData(self.path, 'Placeholder', 2, 9)
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
        logger_setup.logger.info("*** PH is successfully created ***")
        time.sleep(20)

        self.ph.validate_ph_and_revision(phTitle, self.path)
        logger_setup.logger.info("*** Placeholder and its revision successfully validated ***")
        logger_setup.logger.info("*** End of Placeholder creation test ***")
        time.sleep(2)
