import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardTabs, iframes, regDocument_properties
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_Document_Info:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    path = ".//TestData/DataManager.xlsx"
    docTitles = "02-ACM-ARC-MDL-020101"

    logger = LogGen.loggen()

    def test_document_properties(self, setup):
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.dt = DashboardTabs(self.driver)
        self.dp = regDocument_properties(self.driver)
        self.lp = LoginPage(self.driver)

        self.lp.setUsername(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt.clickdocumentmgtab()
        time.sleep(10)

        # will uncomment below code only when to close the window of the preferences menu if already opened.
        # self.dp.click_menu_dropdown(self.widget_name)
        # time.sleep(5)

        self.iframe.navigate_to_tab_registered_document()
        self.logger.info("** Clicked on Registered Documents tab **")
        time.sleep(10)

        self.dp.reg_rows_filter()
        self.logger.info("*** clicked on the filter menu**")
        time.sleep(10)

        docTitles = ExcelUtils.readData(self.path, 'document', 2, 4)
        self.dp.check_doc_properties(docTitles)
        self.logger.info("**** Clicked on Document name****")
        time.sleep(5)

        self.dp.check_doc_revision(docTitles)
        self.logger.info("---- Doc revision scenario complete --- ")
        time.sleep(5)

        # docTitles = ExcelUtils.readData(self.path, 'document', 2, 4)
        # for docTitle in docTitles:
        #     self.iframe.select_a_document(docTitle)
        #     self.logger.info("**** Document Title selected****")
        # time.sleep(5)
        #
        # self.iframe.create_workflow()
        # self.logger.info("*** workflow window opened ***")
        #
        # self.title = ExcelUtils.readData(self.path, 'document', 2, 6)
        # self.iframe.wf_creation_window(self.title)
        # print(self.title)
        # self.logger.info("**** In Wf creation window****")
        # time.sleep(5)

        # self.iframe.start_workflow()
        # self.logger.info("** inside WF start **")
        # time.sleep(5)
