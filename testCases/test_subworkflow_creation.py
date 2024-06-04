import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.LocatorsTransmittal import LoginPage
from pageObjects.LocatorsDocumentAndWorkflow import DashboardAndTabs, worklow_mg
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

class Test_004_SubWorkflow_Creation:
    path = "D://Git//test-automation//feature//Code_merge//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    # username = ReadConfig.getUsername()
    # password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_subworkflow_creation(self,setup):

        self.username = XLUtils.readData(self.path, "Users", 3, 1)
        self.password = XLUtils.readData(self.path, "Users", 3, 2)
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        # self.filter1 = XLUtils.readData(self.path, "Inputs", 2, 2)
        # self.filter2 = XLUtils.readData(self.path, "Inputs", 2, 3)
        self.wf_no = XLUtils.readData(self.path, "Inputs", 2, 14)
        self.assignee = XLUtils.readData(self.path, "Inputs", 2, 4)
        self.swf_title = XLUtils.readData(self.path, "Inputs", 2, 12)
        self.swf_route_template = XLUtils.readData(self.path, "Inputs", 3, 12)
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        # self.content1 = XLUtils.readData(self.path, "Inputs", 2, 4)
        # self.content2 = XLUtils.readData(self.path, "Inputs", 3, 4)

        self.logger.info("*** Starting SubWorkflow Creation test ***")
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        self.dt.dashboardselection(self.dashboard)
        self.logger.info("*** Dashboard is selected ***")

        time.sleep(5)
        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.dt.clickworkflowmgtab()
        self.logger.info("*** Navigated to Workflow Management tab ***")
        time.sleep(5)
        # filter1 = "Completed"
        # filter2 = "Owned By Me"
        self.wf_mg = worklow_mg(self.driver)
        # self.wf_mg.select_WF_filter(self.filter1,self.filter2)
        # time.sleep(20)
        # self.driver.save_screenshot(".\\Screenshots\\subworkflow\\filter_selected.png")
        # time.sleep(20)
        # self.logger.info("** Filter successfully selected **")
        self.wf_mg.select_Workflow(self.wf_no)
        self.logger.info("** Desired Workflow is selected **")
        self.wf_mg.select_inboxTask(self.assignee)
        self.logger.info("** Desired Inbox task is selected **")
        self.wf_mg.click_on_create_swf()
        self.logger.info("** Clicked on Create SWF button **")
        self.wf_mg.select_swf_route_template(self.swf_route_template)
        #self.wf_mg.select_content_s_or_m([self.content1, self.content2])
        self.wf_mg.select_content_all(self.docname1)
        self.logger.info("** all documents are selected **")
        self.wf_mg.create_swf(self.swf_title)
        self.logger.info("** SubWorkflow successfully created **")
        self.wf_mg.start_SWF(self.path)
        time.sleep(20)
        self.wf_mg.validate_started_swf(" Awaiting Comment ")
        self.logger.info("** SubWorkflow successfully Started **")

        self.logger.info("*** Ended SubWorkflow creation test ***")


