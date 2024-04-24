import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.Locators import LoginPage, DashboardAndTabs, worklow_mg,import_comments
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

class Test_008_Update_Comments:
    path = "D://Git//test-automation//3DX_pythonProject//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    # username = ReadConfig.getUsername()
    # password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_update_comments(self,setup):

        self.username = XLUtils.readData(self.path, "Users", 5, 1)
        self.password = XLUtils.readData(self.path, "Users", 5, 2)
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        # self.filter1 = XLUtils.readData(self.path, "Inputs", 2, 2)
        # self.filter2 = XLUtils.readData(self.path, "Inputs", 2, 3)
        self.wf_no = XLUtils.readData(self.path, "Inputs", 2, 14)
        self.swf_no = XLUtils.readData(self.path, "Inputs", 3, 14)
        self.assignee = XLUtils.readData(self.path, "Inputs", 3, 4)
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        self.docname2 = XLUtils.readData(self.path, "Inputs", 3, 8)
        self.attribute = XLUtils.readData(self.path, "Inputs", 2, 19)
        self.status_value = XLUtils.readData(self.path, "Inputs", 3, 19)
        self.comment = XLUtils.readData(self.path, "Inputs", 4, 19)
        self.doc_page = XLUtils.readData(self.path, "Inputs", 5, 19)

        self.logger.info("*** Starting Comment Creation test ***")
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
        self.wf_mg = worklow_mg(self.driver)
        self.wf_mg.expand_Workflow(self.wf_no)
        self.logger.info("** Workflow expanded successfully **")
        self.wf_mg.select_Subworkflow(self.swf_no)
        self.logger.info("** Subworkflow successfully selected **")

        # Updating single comment
        # self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        # self.wf_mg.navigate_to_CRS_mg()
        # self.wf_mg.validate_created_cmt("General comment")
        # self.wf_mg.edit_single_comment("General comment","desc_updated")

        # Updating bulk comments
        self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        self.wf_mg.navigate_to_CRS_mg()

        self.wf_mg.modify_bulk_comments([1], "Initial Status",'C')
        # self.wf_mg.modify_bulk_comments([1],self.attribute,self.status_value,self.comment)

        self.wf_mg.remove_comments([2])
        self.wf_mg.filtered_comments("Remove")


        self.logger.info("*** Ended Importing Comments test ***")

