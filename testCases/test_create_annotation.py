import time
from utilities import XLUtils
import os
from utilities.logger import logger_setup

from pageObjects.LocatorsTransmittal import LoginPage
from pageObjects.LocatorsDashboard import DashboardAndTabs
from pageObjects.LocatorsDocumentAndWorkflow import worklow_mg
from utilities.readProperties import ReadConfig


class Test_018_Create_Annotation:
    # path = ".//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()

    # logger = LogGen.loggen()

    def test_create_annotation(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        self.username = XLUtils.readData(self.path, "Users", 2, 1)
        self.password = XLUtils.readData(self.path, "Users", 5, 2)
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        # self.filter1 = XLUtils.readData(self.path, "Inputs", 2, 2)
        # self.filter2 = XLUtils.readData(self.path, "Inputs", 2, 3)
        self.wf_no = XLUtils.readData(self.path, "Inputs", 2, 14)
        self.swf_no = XLUtils.readData(self.path, "Inputs", 3, 14)
        self.assignee = XLUtils.readData(self.path, "Inputs", 4, 4)
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        self.docname2 = XLUtils.readData(self.path, "Inputs", 3, 8)
        self.desc = XLUtils.readData(self.path, "Inputs", 2, 16)
        self.disciplines = XLUtils.readData_multiple(self.path, "Inputs", 2, 2, 17)
        self.discipline = XLUtils.readData(self.path, "Inputs", 3, 17)
        self.crs_file_path = XLUtils.readData(self.path, "Inputs", 4, 16)
        self.pdf_file_path = XLUtils.readData(self.path, "Inputs", 5, 16)
        self.comment = XLUtils.readData(self.path, "Inputs", 2, 21)
        self.status = XLUtils.readData(self.path, "Inputs", 3, 22)

        logger_setup.logger.info("*** Starting annotation Creation test ***")
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

        time.sleep(3)
        self.dt.clickworkflowmgtab()
        logger_setup.logger.info("*** Clicked on workflow management tab ***")
        time.sleep(5)
        self.wf_mg = worklow_mg(self.driver)
        self.wf_mg.expand_Workflow(self.wf_no)
        logger_setup.logger.info("*** expanded the desired workflow " + self.wf_no + " ***")
        self.wf_mg.select_Subworkflow(self.swf_no)
        logger_setup.logger.info("** Sub-workflow " + self.swf_no + " successfully selected **")
        time.sleep(2)

        self.wf_mg.select_inboxTask(self.assignee)
        logger_setup.logger.info("*** Inbox task selected by " + self.assignee + " ***")

        self.wf_mg.inboxTask_review_comment(self.assignee, self.docname1)
        logger_setup.logger.info("*** Clicked on 'Review and Comment' command by " + self.assignee + " for " + self.docname1 + " ***")

        x1 = 3.66
        y1 = 20.04
        x2 = 180.66
        y2 = 120.74
        self.wf_mg.create_annotation(x1, x2, y1, y2, self.comment, self.status)
        logger_setup.logger.info("*** Annotation created and saved ***")
        time.sleep(20)

        self.wf_mg.validate_annotation(self.comment, self.status)
        time.sleep(5)
        logger_setup.logger.info("*** Annotation successfully validated with comment = " + self.comment + " & status = " + self.status + " ***")
        logger_setup.logger.info("*** Ended Annotation creation test ***")
        # self.logger.info("*** Ended Comment creation test ***")
