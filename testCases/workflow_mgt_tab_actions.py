import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.LocatorsTransmittal import LoginPage, DashboardAndTabs, worklow_mg, import_comments
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig


class Test_009_Workflow_mgt_tab_actions:
    path = ".//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    # username = ReadConfig.getUsername()
    # password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_workflow_mgt_tab_actions(self, setup):
        self.username = XLUtils.readData(self.path, "Users", 5, 1)
        self.password = XLUtils.readData(self.path, "Users", 5, 2)
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        self.wf_no = XLUtils.readData(self.path, "Inputs", 2, 14)
        self.columns = XLUtils.readData_multiple(self.path, "Inputs", 2, 5, 20)

        self.logger.info("*** Starting Comment Creation test ***")
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(5)

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
        # Export workflows in excel
        self.wf_mg.export_Workflows()
        self.logger.info("** Workflow exported successfully in excel**")

        # Export CRS report
        self.wf_mg.select_Workflow(self.wf_no)
        self.logger.info("** Desired Workflow is selected **")
        self.wf_mg.export_CRS()
        self.logger.info("** CRS exported successfully in for desired workflow**")

        # Customize columns visibility
        self.wf_mg.click_on_customize_column_filter()
        for column in self.columns:
            self.wf_mg.customize_column_filter([column])
            # self.logger.info(f"** {column} is selected **")

        self.logger.info("*** Ended workflow actions test ***")
