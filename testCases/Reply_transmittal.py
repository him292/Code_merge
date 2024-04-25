import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardAndTabs, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_Reply_Transmittal:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    logger = LogGen.loggen()

    def test_reply(self, setup):
        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)
        self.lp = LoginPage(self.driver)
        self.dt = DashboardAndTabs(self.driver)
        self.dp = regDocument_properties(self.driver)
        self.tra = Create_Transmittal(self.driver)

        time.sleep(5)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)
        dashboard = "GENERIC Dashboard"
        widget_name = 'Document Register'

        self.logger.info("*** Starting Dashboard Selection test ***")

        traSelect = XLUtils.readData(self.path, 'transmittal', 3, 4)
        tratypeSelect = XLUtils.readData(self.path, 'transmittal', 4, 8)
        to_username = XLUtils.readData(self.path, 'transmittal', 2, 5)
        cc_username = XLUtils.readData(self.path, 'transmittal', 3, 5)
        tra_reason = XLUtils.readData(self.path, 'transmittal', 2, 9)
        traresponse_rqd = XLUtils.readData(self.path, 'transmittal', 2, 10)
        trasubject = XLUtils.readData(self.path, 'transmittal', 2, 11)
        tra_asset = XLUtils.readData(self.path, 'transmittal', 2, 12)
        tra_contract = XLUtils.readData(self.path, 'transmittal', 2, 13)
        tra_wo = XLUtils.readData(self.path, 'transmittal', 2, 14)
        tra_stage = XLUtils.readData(self.path, 'transmittal', 2, 15)
        disciplines = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3,16)
        tra_design = XLUtils.readData(self.path, 'transmittal', 2, 17)
        tra_info = XLUtils.readData(self.path, 'transmittal', 2, 18)
        traMessage = XLUtils.readData(self.path, 'transmittal', 2, 19)
        tra_category = XLUtils.readData(self.path, 'transmittal', 3, 20)
        tra_letter_ini = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3,21)
        # tra_letter_add = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3,22)
        tra_letter_add = XLUtils.readData(self.path, 'transmittal', 2,22)

        time.sleep(5)

        self.dt.dashboardselection(dashboard)
        time.sleep(3)

        # ----- temporary code for reply-transmittal and verifying it

        self.dt.clickmailmgtab()
        time.sleep(10)

        self.tr = transmittal_reply(self.driver)
        self.tr.selecting_sent_filters()
        time.sleep(5)

        self.tr.validate_tra_and_click(traSelect)
        time.sleep(5)

        self.tr.scroll_tra_properties()
        time.sleep(5)

        self.tr.click_reply_command()
        time.sleep(5)

        self.tra.traType_rfi(tratypeSelect)
        time.sleep(5)

        # self.tra.tra_toUser(to_username)
        # time.sleep(10)
        # cc_username = ExcelUtils.readData(self.path, 'transmittal', 3, 5)
        # self.tr.tra_Reply_ccUser(cc_username)
        # time.sleep(10)

        self.tra.traReason(tra_reason)
        time.sleep(3)

        # self.tr.tra_reply_ResponseRequired(traresponse_rqd)
        # time.sleep(3)
        # # #
        # self.tra.traResponseDatePicker()
        # time.sleep(3)
        # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
        # trasubject = ExcelUtils.readData(self.path, 'transmittal', 2, 11)
        # self.tra.tra_Subject(trasubject)
        # time.sleep(5)
        #
        # # # ==================================== for TYPE= TRA & catogory = other than LETTER
        self.tra.tra_category_other(tra_category)
        time.sleep(3)
        # self.tra.tra_contract(tra_contract)
        # time.sleep(3)
        # #
        # self.tra.tra_wo(tra_wo)
        # time.sleep(3)
        #
        for discipline in disciplines:
            self.tra.tra_discipline(discipline)
            self.logger.info(f"** {discipline} is selected **")
            time.sleep(3)
        #
        # # below will be execute when TR Categoty=Letter is selected
        for initiator in tra_letter_ini:
            self.tra.ltr_initiator(initiator)
            self.logger.info(f"** {initiator} is selected **")
            time.sleep(3)

        # for addressee in tra_letter_add:
        #     self.tra.ltr_addressee(addressee)
        #     self.logger.info(f"** {addressee} is selected **")
        #     time.sleep(3)

        self.tra.ltr_addressee(tra_letter_add)
        time.sleep(3)

        self.tra.tra_Message(traMessage)
        time.sleep(3)
        # # ==================================== for TYPE= TRA &  catogory = other than LETTER

        # self.tra.rfi_assetCode(tra_asset)
        # time.sleep(3)
        #
        # self.tra.tra_contract(tra_contract)
        # time.sleep(3)
        # # #
        # self.tra.tra_wo(tra_wo)
        # time.sleep(3)
        #
        # self.tra.rfi_stage(tra_stage)
        # time.sleep(3)
        # #
        #
        # for discipline in disciplines:
        #     self.tra.tra_discipline([discipline])
        #     self.logger.info(f"** {discipline} is selected **")
        # time.sleep(3)
        # #
        # self.tra.rfi_design(tra_design)
        # time.sleep(3)
        #
        # self.tra.rfi_info_requested(tra_info)
        # time.sleep(3)
        #
        # self.tr.tra_reply_Message(traMessage)
        # time.sleep(3)

        # click on REPLY button
        self.tr.tra_reply()
        time.sleep(10)

        # Transmittal Type-RFI ---------------------------------------------------------------------- END
