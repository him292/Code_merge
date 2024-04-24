import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardAndTabs, regDocument_properties, documentRegisterAndWorkflow
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_006_Dashboard_selection:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    path = "D://Git//test-automation//3DX_pythonProject//TestData//DataManager.xlsx"
    #docTitles = "02-ACM-ARC-MDL-020101"

    logger = LogGen.loggen()

    def test_document_properties(self, setup):
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)
        time.sleep(5)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        time.sleep(5)

        self.dt.clickdocumentmgtab()
        time.sleep(5)

        self.dt.click_menu_dropdown(self.widget_name)
        time.sleep(5)

        self.dt.maximize_widget(self.widget_name)

        self.docReg_Wf = documentRegisterAndWorkflow(self.driver)

        self.docReg_Wf.navigate_to_tab_registered_document()
        self.logger.info("** Clicked on Registered Documents tab **")
        time.sleep(10)

        # self.dp.reg_rows_filter()
        # self.logger.info("*** clicked on the filter menu**")
        # time.sleep(10)

        self.dp = regDocument_properties(self.driver)
        time.sleep(5)

        # docTitles = "02-ACM-ARC-MDL-020101"
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        self.dp.check_doc_properties(self.docname1)
        self.logger.info("**** Clicked on Document name****")
        time.sleep(5)

        self.dp.check_doc_revision(self.docname1)
        self.logger.info("---- Doc revision scenario complete --- ")
        time.sleep(5)

