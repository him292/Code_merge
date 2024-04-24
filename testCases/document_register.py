import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.Locators import LoginPage, DashboardAndTabs, documentRegisterAndWorkflow
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

class Test_003_Document_Register:
    path = "D://Git//test-automation//3DX_pythonProject//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    #filepath = "C://Users//Lenovo//Desktop//sample_files//02-DAH-LAN-3DM-245003_A.pdf"

    logger = LogGen.loggen()


    def test_Document_register(self,setup):

        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        self.widget_name = XLUtils.readData(self.path, "Inputs", 2, 2)
        self.folder_path = XLUtils.readData(self.path, "Inputs",2 , 6)
        self.title = XLUtils.readData(self.path, "Inputs", 3, 6)
        self.wo_number = XLUtils.readData(self.path, "Inputs",4 , 6)
        self.status = XLUtils.readData(self.path, "Inputs", 5, 6)
        self.stage = XLUtils.readData(self.path, "Inputs", 6, 6)

        self.logger.info("*** Starting Document Register test ***")
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)
        time.sleep(2)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)

        self.dt = DashboardAndTabs(self.driver)
        # self.logger.info("*** Starting Dashboard Selection test ***")
        self.dt.dashboardselection(self.dashboard)
        time.sleep(5)
        self.dt.clickworkflowmgtab()
        time.sleep(2)
        self.dt.clickdocumentmgtab()
        time.sleep(2)
        self.dt.click_menu_dropdown(self.widget_name)
        self.dt.maximize_widget(self.widget_name)

        self.docReg_Wf = documentRegisterAndWorkflow(self.driver)
        self.docReg_Wf.navigate_to_tab_document_upload()
        self.logger.info("** Clicked on Document Upload tab **")
        time.sleep(5)
        self.docReg_Wf.select_file(self.folder_path)
        time.sleep(5)
        self.driver.save_screenshot("D:\\Git//test-automation\\3DX_pythonProject\\Screenshots\\DocReg_screenshots\\fileuploaded.png")
        self.logger.info("** file is uploaded 100% **")
        self.docReg_Wf.store_file_names(self.path,self.folder_path)

        self.docReg_Wf.open_document_edit_form()
        self.logger.info("** Document mass edit form is opened **")
        self.docReg_Wf.update_document_title(self.title)
        self.logger.info("*** Title entered successfully ***")
        self.docReg_Wf.update_document_workorder(self.wo_number)
        self.logger.info("*** Work Order successfully selected***")
        self.docReg_Wf.update_document_status(self.status)
        self.logger.info("*** Status successfully selected***")
        self.docReg_Wf.update_document_stage(self.stage)
        self.driver.save_screenshot(
            "D:\\Git//test-automation\\3DX_pythonProject\\Screenshots\\DocReg_screenshots\\detailsUpdated.png")
        self.logger.info("*** Stage successfully selected***")
        self.docReg_Wf.test_save_document()
        self.logger.info("*** Clicked on SAVE button ***")
        self.docReg_Wf.navigate_to_tab_registered_document()
        self.docname1 = XLUtils.readData(self.path, "Inputs", 2, 8)
        self.docname2 = XLUtils.readData(self.path, "Inputs", 3, 8)
        self.docReg_Wf.validate_reg_documents([self.docname1, self.docname2])
        self.logger.info(f"{self.docname1} and {self.docname2} are displayed")
        time.sleep(5)
        self.logger.info("** Document Successfully Registered **")
        self.logger.info("*** Ended Navigate Document Management tab test ***")

