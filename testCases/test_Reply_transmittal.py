import time
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsTransmittal import LoginPage, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from pageObjects.LocatorsDashboard import DashboardAndTabs
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_012_Reply_Transmittal:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    # path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    # logger = LogGen.loggen()

    def test_reply(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        logger_setup.logger.info("*** Starting transmittal REPLY test ***")
        logger_setup.logger.info("*** login to the platform ***")
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
        logger_setup.logger.info("*** Login is successful ***")
        time.sleep(10)
        dashboard = "GENERIC Dashboard"

        traSelect = XLUtils.readData(self.path, 'transmittal', 3, 4)
        tratypeSelect = XLUtils.readData(self.path, 'transmittal', 2, 8)
        to_username = XLUtils.readData(self.path, 'transmittal', 2, 5)
        cc_username = XLUtils.readData(self.path, 'transmittal', 3, 5)
        tra_reason = XLUtils.readData(self.path, 'transmittal', 2, 9)
        traresponse_rqd = XLUtils.readData(self.path, 'transmittal', 2, 10)
        trasubject = XLUtils.readData(self.path, 'transmittal', 2, 11)
        tra_asset = XLUtils.readData(self.path, 'transmittal', 2, 12)
        tra_contract = XLUtils.readData(self.path, 'transmittal', 2, 13)
        tra_wo = XLUtils.readData(self.path, 'transmittal', 2, 14)
        tra_stage = XLUtils.readData(self.path, 'transmittal', 2, 15)
        disciplines = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3, 16)
        tra_design = XLUtils.readData(self.path, 'transmittal', 2, 17)
        tra_info = XLUtils.readData(self.path, 'transmittal', 2, 18)
        traMessage = XLUtils.readData(self.path, 'transmittal', 2, 19)
        tra_category = XLUtils.readData(self.path, 'transmittal', 3, 20)
        tra_letter_ini = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3, 21)
        tra_letter_add = XLUtils.readData_multiple(self.path, 'transmittal', 2, 3, 22)

        time.sleep(5)

        self.dt.dashboardselection(dashboard)
        logger_setup.logger.info("*** Dashboard selected ***")
        time.sleep(3)

        # ----- temporary code for reply-transmittal and verifying it

        self.dt.clickmailmgtab()
        logger_setup.logger.info("*** Navigated to Mail Management tab ***")
        time.sleep(10)

        self.tr = transmittal_reply(self.driver)
        self.tr.selecting_sent_filters()
        logger_setup.logger.info("*** Desired filters are applied ***")
        time.sleep(5)

        self.tr.validate_tra_and_click(traSelect)
        logger_setup.logger.info("*** Transmittal " + traSelect + " is validated and opened ***")
        time.sleep(5)

        self.tr.scroll_tra_properties()
        time.sleep(5)

        self.tr.click_reply_command()
        logger_setup.logger.info("*** User has decided to REPLY to the Transmittal ***")
        time.sleep(5)

        self.tra.traType_rfi(tratypeSelect)
        logger_setup.logger.info("*** TRA of type " + tratypeSelect + " is selected ***")
        time.sleep(5)

        self.tra.tra_toUser(to_username)
        time.sleep(10)
        # cc_username = ExcelUtils.readData(self.path, 'transmittal', 3, 5)
        # self.tr.tra_Reply_ccUser(cc_username)
        # time.sleep(10)

        if tratypeSelect == "GCD":
            self.tra.traResponseRequired_reply_fwd(traresponse_rqd)
            logger_setup.logger.info("*** Response required is set to YES ***")
            time.sleep(3)
            # #
            self.tra.traResponseDatePicker()
            time.sleep(3)
            # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
            # trasubject = ExcelUtils.readData(self.path, 'transmittal', 2, 11)
            # self.tra.tra_Subject(trasubject)
            # time.sleep(5)
            self.tr.tra_reply_Message(traMessage)
            time.sleep(1)
            self.tr.tra_reply()
            logger_setup.logger.info("*** Transmittal is successfully replied ***")
            logger_setup.logger.info("*** End of TRA Reply test ***")
            time.sleep(5)
        elif tratypeSelect == "TRA":
            self.tra.traReason_reply_fwd(tra_reason)
            time.sleep(3)
            self.tra.traResponseRequired_reply_fwd(traresponse_rqd)
            logger_setup.logger.info("*** Response required is set to YES ***")
            time.sleep(3)
            # #
            self.tra.traResponseDatePicker()
            time.sleep(3)
            # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
            # trasubject = ExcelUtils.readData(self.path, 'transmittal', 2, 11)
            # self.tra.tra_Subject(trasubject)
            # time.sleep(5)

            # # # ==================================== for TYPE= TRA & catogory = LETTER or other
            self.tra.tra_category_ltr(tra_category)
            time.sleep(1)
            self.tra.tra_contract(tra_contract)
            time.sleep(3)
            #
            self.tra.tra_wo(tra_wo)
            time.sleep(3)

            self.tra.tra_discipline(disciplines)
            time.sleep(3)
            if tra_category == "Letter":
                self.tra.ltr_initiator(tra_letter_ini)
                time.sleep(3)
                self.tra.ltr_addressee(tra_letter_add)
                time.sleep(3)
            self.tr.tra_reply_Message(traMessage)
            time.sleep(3)
            # click on REPLY button
            self.tr.tra_reply()
            logger_setup.logger.info("*** Transmittal is successfully replied ***")
            logger_setup.logger.info("*** End of TRA Reply test ***")
            time.sleep(5)
        else:  # the tratypeSelect == RFI
            self.tra.traResponseRequired_reply_fwd(traresponse_rqd)
            logger_setup.logger.info("*** Response required is set to YES ***")
            time.sleep(3)
            # #
            self.tra.traResponseDatePicker()
            time.sleep(1)
            # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
            # self.tra.tra_Subject(trasubject)
            # time.sleep(1)
            self.tra.rfi_assetCode(tra_asset)
            time.sleep(1)

            self.tra.tra_contract(tra_contract)
            time.sleep(1)
            # #
            self.tra.tra_wo(tra_wo)
            time.sleep(1)

            self.tra.rfi_stage(tra_stage)
            time.sleep(1)
            #

            for discipline in disciplines:
                self.tra.tra_discipline([discipline])
                logger_setup.logger.info(f"** {discipline} is selected **")
            time.sleep(3)
            #
            self.tra.rfi_design(tra_design)
            time.sleep(3)

            self.tra.rfi_info_requested(tra_info)
            time.sleep(3)

            self.tr.tra_reply_Message(traMessage)
            time.sleep(3)

            # # click on REPLY button
            # self.tr.tra_reply()
            # logger_setup.logger.info("*** Transmittal is successfully replied ***")
            # logger_setup.logger.info("*** End of TRA Reply test ***")
            # time.sleep(5)

        # Transmittal Type-RFI ---------------------------------------------------------------------- END
