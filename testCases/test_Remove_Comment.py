import time
from utilities import XLUtils
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsTransmittal import LoginPage, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from pageObjects.LocatorsDocumentAndWorkflow import worklow_mg
from pageObjects.LocatorsDashboard import DashboardAndTabs
from utilities.readProperties import ReadConfig


class Test_021_Remove_Comment:
    base_dir = ReadConfig.get_base_dir()
    path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
    baseURL = ReadConfig.getURL()

    def test_remove_comment(self, setup):
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
        self.status = XLUtils.readData(self.path, "Inputs", 3, 16)
        self.disciplines = XLUtils.readData_multiple(self.path, "Inputs", 2, 2, 17)
        self.discipline = XLUtils.readData(self.path, "Inputs", 3, 17)
        self.crs_file_path = XLUtils.readData(self.path, "Inputs", 4, 16)
        self.pdf_file_path = XLUtils.readData(self.path, "Inputs", 5, 16)

        logger_setup.logger.info("*** Starting Comment Creation test ***")
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
        self.wf_mg.expand_Workflow(self.wf_no)
        logger_setup.logger.info("** Workflow expanded successfully **")
        self.wf_mg.select_Subworkflow(self.swf_no)
        logger_setup.logger.info("** Subworkflow successfully selected **")

        # Create general comments
        self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        self.wf_mg.click_on_create_comment()
        self.wf_mg.create_cmt(self.desc, self.status)
        self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        self.wf_mg.navigate_to_CRS_mg()
        self.wf_mg.validate_created_cmt(self.desc)
        time.sleep(2)
