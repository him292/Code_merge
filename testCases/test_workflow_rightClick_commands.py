import time
import os
from utilities import XLUtils
from utilities.logger import logger_setup
from pageObjects.LocatorsTransmittal import LoginPage
from pageObjects.LocatorsDashboard import DashboardAndTabs
from pageObjects.LocatorsDocumentAndWorkflow import worklow_mg
from utilities.readProperties import ReadConfig


class Test_017_workflow_rightClick_Commands:
    # path = ".//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()

    # logger = LogGen.loggen()

    def test_workflow_rightClick_Commands(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        self.username = XLUtils.readData(self.path, "Users", 2, 1)
        self.password = XLUtils.readData(self.path, "Users", 2, 2)
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        # self.filter1 = XLUtils.readData(self.path, "Inputs", 2, 2)
        # self.filter2 = XLUtils.readData(self.path, "Inputs", 2, 3)
        self.wf_no = XLUtils.readData(self.path, "Inputs", 2, 14)
        self.swf_no = XLUtils.readData(self.path, "Inputs", 3, 14)
        self.assignee = XLUtils.readData(self.path, "Inputs", 4, 4)
        self.swf_title = XLUtils.readData(self.path, "Inputs", 2, 12)
        self.swf_route_template = XLUtils.readData(self.path, "Inputs", 3, 12)
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        # self.content1 = XLUtils.readData(self.path, "Inputs", 2, 4)
        # self.content2 = XLUtils.readData(self.path, "Inputs", 3, 4)

        logger_setup.logger.info("*** Document right click commands test ***")
        logger_setup.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        logger_setup.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        self.dt.dashboardselection(self.dashboard)
        logger_setup.logger.info("*** Dashboard is selected ***")

        time.sleep(5)
        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.dt.clickworkflowmgtab()
        logger_setup.logger.info("*** Navigated to Workflow Management tab ***")
        time.sleep(5)
        self.wf_mg = worklow_mg(self.driver)
        self.wf_mg.select_Workflow(self.wf_no)
        logger_setup.logger.info("** Desired Workflow " + self.wf_no + " is selected **")
        self.wf_mg.expand_Workflow(self.wf_no)
        logger_setup.logger.info("*** expanded the desired workflow ***")
        self.wf_mg.select_Subworkflow(self.swf_no)
        logger_setup.logger.info("** Sub-workflow " + self.swf_no + " successfully selected **")
        self.wf_mg.select_inboxTask(self.assignee)
        logger_setup.logger.info("** Desired Inbox task is selected by " + self.assignee + " **")
        self.wf_mg.inboxTask_doc_preview(self.assignee,self.docname1)
        logger_setup.logger.info("** Document Preview is launched by " + self.assignee + " for " + self.docname1 + " **")
        self.wf_mg.inboxTask_review_comment(self.assignee,self.docname1)
        logger_setup.logger.info("** Review and Comment is launched by " + self.assignee + " for " + self.docname1 + " **")
        logger_setup.logger.info("** End of Workflow Commands tests **")

