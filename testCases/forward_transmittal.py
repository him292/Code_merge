import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardTabs, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import ExcelUtils


class Test_Reply_Transmittal:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    # widget_name = 'Workflow Management'
    # path = ".//TestData/LoginDataSheet.xlsx"
    path = "D://Git//test-automation//feature//Code_merge//TestData//DataManager.xlsx"
    # docTitles = ["02-DAH-LAN-3DM-245004", "02-ABI-BMN-3DM-000011"]
    docTitles = "02-CH2-STR-MDL-900123"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    traRespReqd = ExcelUtils.readData(path, 'transmittal', 4, 7)
    traSubject = ExcelUtils.readData(path, 'transmittal', 5, 7)
    traCategory = ExcelUtils.readData(path, 'transmittal', 6, 7)
    traContract = ExcelUtils.readData(path, 'transmittal', 7, 7)
    traWO = ExcelUtils.readData(path, 'transmittal', 8, 7)
    traDiscipline = ExcelUtils.readData(path, 'transmittal', 9, 7)
    traMessage = ExcelUtils.readData(path, 'transmittal', 10, 7)

    logger = LogGen.loggen()

    def test_reply(self, setup):
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.lp = LoginPage(self.driver)
        self.dt = DashboardTabs(self.driver)
        self.dp = regDocument_properties(self.driver)
        self.tra = Create_Transmittal(self.driver)

        time.sleep(5)
        self.lp.setUsername(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)
        dashboard = "GENERIC Dashboard"
        widget_name = 'Document Register'

        self.logger.info("*** Starting Dashboard Selection test ***")

        time.sleep(5)

        self.dt.dashboard_selection(dashboard)
        time.sleep(3)

        # Transmittal - FORWARD - Code ---------------------------------------------------------- START

        self.dt.clickmailmgtab()
        time.sleep(10)

        self.tr = transmittal_reply(self.driver)

        self.tr.selecting_Inbox_filters()
        time.sleep(5)

        traSelect = ExcelUtils.readData(self.path, 'transmittal', 3, 4)
        self.tr.validate_tra_and_click(traSelect)
        time.sleep(5)

        # self.tr.scroll_tra_properties()
        # time.sleep(5)
        #
        self.tr.click_forward_command()
        time.sleep(5)
        #
        tratypeSelect = ExcelUtils.readData(self.path, 'transmittal', 2, 8)
        self.tra.traType_rfi(tratypeSelect)
        time.sleep(5)
        #
        to_username = ExcelUtils.readData(self.path, 'transmittal', 2, 5)
        self.tr.tra_fwd_toUser(to_username)
        time.sleep(10)
        # cc_username = ExcelUtils.readData(self.path, 'transmittal', 3, 5)
        # self.tr.tra_Reply_ccUser(cc_username)
        # time.sleep(10)
        traresponse_rqd = ExcelUtils.readData(self.path, 'transmittal', 2, 10)
        self.tr.tra_reply_ResponseRequired(traresponse_rqd)
        time.sleep(3)
        # #
        self.tra.traResponseDatePicker()
        time.sleep(3)

        # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
        # trasubject = ExcelUtils.readData(self.path, 'transmittal', 2, 11)
        # self.tra.tra_Subject(trasubject)
        # time.sleep(5)

        tra_asset = ExcelUtils.readData(self.path, 'transmittal', 2, 12)
        self.tra.rfi_assetCode(tra_asset)
        time.sleep(3)

        tra_contract = ExcelUtils.readData(self.path, 'transmittal', 2, 13)
        self.tra.tra_contract(tra_contract)
        time.sleep(3)
        # #
        tra_wo = ExcelUtils.readData(self.path, 'transmittal', 2, 14)
        self.tra.tra_wo(tra_wo)
        time.sleep(3)
        #
        tra_stage = ExcelUtils.readData(self.path, 'transmittal', 2, 15)
        self.tra.rfi_stage(tra_stage)
        time.sleep(3)
        #
        # val = ['AVC - Audio Visual', 'ARC - Architectural']
        disciplines_list = ExcelUtils.readData_multiple(self.path, 'transmittal', 2, 3, 16)
        # Iterate through each discipline value and call tra_discipline for each one
        for discipline_value in disciplines_list:
            self.tr.tra_fwd_discipline(discipline_value)
        time.sleep(2)

        # #
        tra_design = ExcelUtils.readData(self.path, 'transmittal', 2, 17)
        self.tra.rfi_design(tra_design)
        time.sleep(3)

        tra_info = ExcelUtils.readData(self.path, 'transmittal', 2, 18)
        self.tra.rfi_info_requested(tra_info)
        time.sleep(3)

        traMessage = ExcelUtils.readData(self.path, 'transmittal', 2, 19)
        self.tr.tra_reply_Message(traMessage)
        time.sleep(3)

        # click on REPLY button
        self.tr.tra_forward()
        time.sleep(10)

        # Transmittal - FORWARD - Code ---------------------------------------------------------- END

        # docTitles = ExcelUtils.readData(self.path, 'transmittal', 2, 4)
        # self.iframe.tra_send(docTitles)
        # time.sleep(10)
