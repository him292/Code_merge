import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.Locators import LoginPage, DashboardAndTabs, documentRegisterAndWorkflow
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

class Test_004_Workflow_Creation:
    path = "D://Git//test-automation//3DX_pythonProject//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_workflow_creation(self,setup):

        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        self.widget_name = XLUtils.readData(self.path, "Inputs", 2, 2)
        # self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        # self.docname2 = XLUtils.readData(self.path, "Inputs", 3, 8)
        self.documents = XLUtils.readData_multiple(self.path, "Inputs", 2, 3, 8)
        self.wf_title = XLUtils.readData(self.path, "Inputs", 2, 10)
        self.reasonforissue = XLUtils.readData(self.path, "Inputs",3, 10)
        self.wf_route_template = XLUtils.readData(self.path, "Inputs", 4, 10)

        self.logger.info("*** Starting Workflow Creation test ***")
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)
        # self.logger.info("*** Starting Dashboard Selection test ***")

        self.dt = DashboardAndTabs(self.driver)
        self.dt.dashboardselection(self.dashboard)
        self.logger.info("*** Dashboard is selected ***")

        time.sleep(5)
        self.dt.clickworkflowmgtab()
        time.sleep(5)
        self.dt.clickdocumentmgtab()
        self.logger.info("*** Navigated to Document Management tab ***")
        time.sleep(10)
        self.dt.click_menu_dropdown(self.widget_name)
        self.dt.maximize_widget(self.widget_name)

        self.docReg_Wf = documentRegisterAndWorkflow(self.driver)
        self.docReg_Wf.navigate_to_tab_registered_document()
        self.logger.info("** Clicked on Registered Document tab **")
        try:
            for document in self.documents:
                self.docReg_Wf.select_document(document)
            self.logger.info("** documents are selected**")
        except Exception as e:
            raise

        # self.docReg_Wf.select_document(self.docname1)
        # self.logger.info("** doc is selected**")
        # self.docReg_Wf.select_document(self.docname2)
        # self.logger.info("** doc1 is selected**")
        time.sleep(5)
        self.docReg_Wf.click_on_create_wf()
        self.docReg_Wf.select_wf_route_template(self.wf_route_template)
        self.logger.info("** Route Template selected **")
        self.docReg_Wf.create_wf(self.wf_title,self.reasonforissue)
        self.logger.info("** Workflow successfully created **")
        self.docReg_Wf.start_WF(self.path)
        time.sleep(20)
        self.docReg_Wf.validate_started_wf(" Awaiting Approval ")
        self.logger.info("** Workflow successfully Started **")

        self.logger.info("*** Ended Workflow creation test ***")

