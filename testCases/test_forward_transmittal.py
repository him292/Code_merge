import time
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsTransmittal import LoginPage, iframes, regDocument_properties, transmittal_reply
from pageObjects.LocatorsTransmittal import Create_Transmittal
from pageObjects.LocatorsDashboard import DashboardAndTabs
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_013_Forward_Transmittal:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    base_dir = ReadConfig.get_base_dir()
    widget_name = 'Document Register'
    # path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"
    path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
    tratypeSelect = XLUtils.readData(path, 'transmittal', 3, 8)
    to_username = XLUtils.readData(path, 'transmittal', 2, 5)
    # cc_username = ExcelUtils.readData(self.path, 'transmittal', 3, 5)
    traresponse_rqd = XLUtils.readData(path, 'transmittal', 2, 10)
    # trasubject = ExcelUtils.readData(path, 'transmittal', 2, 11)
    tra_asset = XLUtils.readData(path, 'transmittal', 2, 12)
    tra_contract = XLUtils.readData(path, 'transmittal', 2, 13)
    tra_wo = XLUtils.readData(path, 'transmittal', 2, 14)
    tra_stage = XLUtils.readData(path, 'transmittal', 2, 15)
    disciplines_list = XLUtils.readData_multiple(path, 'transmittal', 2, 3, 16)
    tra_design = XLUtils.readData(path, 'transmittal', 2, 17)
    tra_info = XLUtils.readData(path, 'transmittal', 2, 18)
    traMessage = XLUtils.readData(path, 'transmittal', 2, 19)

    # logger = LogGen.loggen()

    def test_forward(self, setup):
        logger_setup.logger.info("*** Starting transmittal FORWARD test ***")
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

        self.dt.dashboardselection(dashboard)
        time.sleep(3)
        logger_setup.logger.info("*** Dashboard selected ***")

        # Transmittal - FORWARD - Code ---------------------------------------------------------- START

        self.dt.clickmailmgtab()
        logger_setup.logger.info("*** Navigated to Mail Management tab ***")
        time.sleep(10)

        self.tr = transmittal_reply(self.driver)

        self.tr.selecting_Inbox_filters()
        logger_setup.logger.info("*** Desired filters are applied ***")
        time.sleep(5)

        traSelect = XLUtils.readData(self.path, 'transmittal', 3, 4)
        self.tr.validate_tra_and_click(traSelect)
        logger_setup.logger.info("*** Transmittal " + traSelect + " is validated and opened ***")
        time.sleep(5)

        # self.tr.scroll_tra_properties()
        # time.sleep(5)
        #
        self.tr.click_forward_command()
        logger_setup.logger.info("*** User has decided to FORWARD the Transmittal ***")
        time.sleep(5)
        #
        self.tra.traType_rfi(self.tratypeSelect)
        logger_setup.logger.info("*** TRA of type " + self.tratypeSelect + " is selected ***")
        time.sleep(5)
        #
        self.tr.tra_fwd_toUser(self.to_username)
        time.sleep(10)
        # self.tr.tra_Reply_ccUser(self.cc_username)
        # time.sleep(10)

        if self.tratypeSelect == "GCD":
            self.tra.traResponseRequired_reply_fwd(self.traresponse_rqd)
            logger_setup.logger.info("*** Response required is set to YES ***")
            time.sleep(3)
            # # #
            self.tra.traResponseDatePicker()
            time.sleep(3)

            # For Reply, no need of Subject, if need to, then add a subject with a prefix of "RE: "
            # self.tra.tra_Subject(self.trasubject)
            # time.sleep(5)
            self.tr.tra_reply_Message(self.traMessage)
            time.sleep(1)
            # click on FORWARD button
            self.tr.tra_forward()
            logger_setup.logger.info("*** Transmittal is successfully forwarded ***")
            logger_setup.logger.info("*** End of TRA Forward test ***")
            time.sleep(10)
        elif self.tratypeSelect == "TRA":
            self.tra.traReason_reply_fwd(self.tra_reason)
            time.sleep(3)
            self.tra.traResponseRequired_reply_fwd(self.traresponse_rqd)
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
            self.tra.tra_category_ltr(self.tra_category)
            time.sleep(1)
            self.tra.tra_contract(self.tra_contract)
            time.sleep(3)
            #
            self.tra.tra_wo(self.tra_wo)
            time.sleep(3)

            self.tra.tra_discipline(self.disciplines)
            time.sleep(3)
            if self.tra_category == "Letter":
                self.tra.ltr_initiator(self.tra_letter_ini)
                time.sleep(3)
                self.tra.ltr_addressee(self.tra_letter_add)
                time.sleep(3)
            self.tr.tra_reply_Message(self.traMessage)
            time.sleep(3)
            # click on FORWARD button
            self.tr.tra_forward()
            logger_setup.logger.info("*** Transmittal is successfully forwarded ***")
            logger_setup.logger.info("*** End of TRA Forward test ***")
            time.sleep(10)
        else:
            self.tra.traResponseRequired_reply_fwd(self.traresponse_rqd)
            logger_setup.logger.info("*** Response required is set to YES ***")
            time.sleep(3)
            # #
            self.tra.traResponseDatePicker()
            time.sleep(3)
            self.tra.rfi_assetCode(self.tra_asset)
            time.sleep(3)

            self.tra.tra_contract(self.tra_contract)
            time.sleep(3)
            # #
            self.tra.tra_wo(self.tra_wo)
            time.sleep(3)
            #
            self.tra.rfi_stage(self.tra_stage)
            time.sleep(3)

            # Iterate through each discipline value and call tra_discipline for each one
            self.tra.tra_discipline(self.disciplines_list)
            time.sleep(2)
            self.tra.rfi_design(self.tra_design)
            time.sleep(3)
            self.tra.rfi_info_requested(self.tra_info)
            time.sleep(3)
            self.tr.tra_reply_Message(self.traMessage)
            time.sleep(3)

            # click on FORWARD button
            self.tr.tra_forward()
            logger_setup.logger.info("*** Transmittal is successfully forwarded ***")
            logger_setup.logger.info("*** End of TRA Forward test ***")
            time.sleep(10)

        # Transmittal - FORWARD - Code ---------------------------------------------------------- END

