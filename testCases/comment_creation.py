import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.Locators import LoginPage, DashboardAndTabs, worklow_mg,import_comments
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

class Test_005_Comment_Creation:
    path = ".//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    # username = ReadConfig.getUsername()
    # password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_subworkflow_creation(self,setup):

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
        self.desc = XLUtils.readData(self.path, "Inputs", 2, 16)
        self.status = XLUtils.readData(self.path, "Inputs", 3, 16)
        self.disciplines = XLUtils.readData_multiple(self.path, "Inputs", 2,2, 17)
        self.discipline = XLUtils.readData(self.path, "Inputs", 3, 17)
        self.crs_file_path = XLUtils.readData(self.path, "Inputs", 4, 16)
        self.pdf_file_path = XLUtils.readData(self.path, "Inputs", 5, 16)

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

        # Create general comments
        # self.wf_mg.select_doc_under_task(self.assignee,self.docname1)
        # self.wf_mg.click_on_create_comment()
        # self.wf_mg.create_cmt(self.desc,self.status)
        # self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        # self.wf_mg.navidate_to_CRS_mg()
        # self.wf_mg.validate_created_cmt(self.desc)
        time.sleep(2)

        self.wf_mg.select_inboxTask(self.assignee)
        self.logger.info("** Desired Inbox task is selected **")

        # self.import_comment = import_comments(self.driver)
        #
        # self.import_comment.click_on_export_CRS_Template()
        # #
        # for discipline in self.disciplines:
        #     self.import_comment.select_disp([discipline])
        #     self.logger.info(f"** {discipline} is selected **")
        #
        # self.import_comment.click_on_save()
        # time.sleep(5)
        # self.logger.info("** File is downloaded **")
        # self.import_comment.click_on_Import_Comments()
        # self.import_comment.browse_CRS_file(self.crs_file_path)
        # self.import_comment.browse_annotation_file(self.pdf_file_path)
        # self.import_comment.click_on_Save_Import_Comments()
        # self.import_comment.validate_CRS_Comments_icon(self.assignee)

        self.wf_mg.select_doc_under_task(self.assignee, self.docname1)
        self.wf_mg.navidate_to_CRS_mg()
        self.wf_mg.validate_created_cmt("Import comment 3")
        self.wf_mg.edit_single_comment("Import comment 3","desc_updated")

        self.logger.info("*** Ended Comment creation test ***")

