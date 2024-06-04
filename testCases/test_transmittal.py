import time
import os
from utilities.logger import logger_setup
from pageObjects.LocatorsTransmittal import LoginPage, iframes, regDocument_properties, Create_Transmittal
from pageObjects.LocatorsDashboard import DashboardAndTabs
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_011_Transmittal:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    # path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    # logger = LogGen.loggen()

    def test_create_Transmittal(self, setup, base_dir):
        self.path = os.path.join(base_dir, "TestData", "DataManager.xlsx")
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
        logger_setup.logger.info("*** Starting Transmittal Creation test ***")
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
        disciplines = XLUtils.readData(self.path, 'transmittal', 2, 16)
        tra_design = XLUtils.readData(self.path, 'transmittal', 2, 17)
        tra_info = XLUtils.readData(self.path, 'transmittal', 2, 18)
        traMessage = XLUtils.readData(self.path, 'transmittal', 2, 19)
        tra_category = XLUtils.readData(self.path, 'transmittal', 2, 20)
        tra_letter_ini = XLUtils.readData(self.path, 'transmittal', 2, 21)
        tra_letter_add = XLUtils.readData(self.path, 'transmittal', 2, 22)

        time.sleep(5)

        self.dt.dashboardselection(self.dashboard)
        time.sleep(3)

        self.dt.clickdocumentmgtab()
        logger_setup.logger.info("*** Clicked on Document management tab ***")
        time.sleep(10)

        # self.lp.click_menu_dropdown(self.widget_name)
        # time.sleep(5)

        self.iframe.navigate_to_tab_registered_document()
        time.sleep(10)

        # self.dp.reg_rows_filter()
        # time.sleep(10)

        docTitles = XLUtils.readData(self.path, 'transmittal', 2, 4)
        # for docTitle in docTitles:
        self.iframe.select_a_document(docTitles)
        logger_setup.logger.info("*** Document " + docTitles + " is selected ***")
        time.sleep(5)

        self.tra.create_transmittal_button()
        time.sleep(5)

        # traTypeSelect = XLUtils.readData(self.path, 'Sheet1', row_num, column_num)  # Assuming row_num and column_num are defined

        # Transmittal Type-GCD/RFI/TRA -- START=======================================================
        self.tra.traType_transmittal(tratypeSelect)
        time.sleep(5)
        self.tra.tra_toUser(to_username)
        time.sleep(10)
        # self.tra.tra_ccUser(cc_username)
        # time.sleep(10)
        if tratypeSelect == "GCD":
            self.tra.traResponseRequired(traresponse_rqd)
            time.sleep(3)
            self.tra.traResponseDatePicker()
            time.sleep(3)
            self.tra.tra_Subject(trasubject)
            time.sleep(1)
            self.tra.tra_Message(traMessage)
            # Include the remaining code outside the if-elif block if it's common for both cases
            docTitles = XLUtils.readData(self.path, 'transmittal', 2, 4)
            self.tra.tra_send()
            logger_setup.logger.info("*** Transmittal is created successfully ***")
            time.sleep(5)
        elif tratypeSelect == "TRA":
            self.tra.traReason(tra_reason)
            time.sleep(1)
            self.tra.traResponseRequired(traresponse_rqd)
            time.sleep(1)
            self.tra.traResponseDatePicker()
            time.sleep(1)
            self.tra.tra_Subject(trasubject)
            time.sleep(1)
            self.tra.tra_category_ltr(tra_category)
            time.sleep(1)
            # ==================================== for catogory = Letter
            self.tra.tra_contract(tra_contract)
            time.sleep(3)
            #
            self.tra.tra_wo(tra_wo)
            time.sleep(3)
            #
            self.tra.tra_discipline(disciplines)
            time.sleep(3)
            if tra_category == "Letter":
                self.tra.ltr_initiator(tra_letter_ini)
                time.sleep(3)
                self.tra.ltr_addressee(tra_letter_add)
                time.sleep(3)

            self.tra.tra_Message(traMessage)
            # Include the remaining code outside the if-elif block if it's common for both cases
            # docTitles = XLUtils.readData(self.path, 'transmittal', 2, 4)
            # self.tra.tra_send()
            # logger_setup.logger.info("*** Transmittal is created successfully ***")
            # time.sleep(5)
        else:  # the tratypeSelect == RFI
            self.tra.traResponseRequired(traresponse_rqd)
            time.sleep(1)
            self.tra.traResponseDatePicker()
            time.sleep(1)
            self.tra.tra_Subject(trasubject)
            time.sleep(2)
            self.tra.rfi_assetCode(tra_asset)
            time.sleep(1)
            self.tra.tra_contract(tra_contract)
            time.sleep(1)
            self.tra.tra_wo(tra_wo)
            time.sleep(1)
            self.tra.rfi_stage(tra_stage)
            time.sleep(1)
            self.tra.tra_discipline(disciplines)
            time.sleep(1)
            self.tra.rfi_design(tra_design)
            time.sleep(1)
            self.tra.rfi_info_requested(tra_info)
            time.sleep(1)
            self.tra.tra_Message(traMessage)
            # Include the remaining code outside the if-elif block if it's common for both cases
            # docTitles = XLUtils.readData(self.path, 'transmittal', 2, 4)
            # self.tra.tra_send()
            # logger_setup.logger.info("*** Transmittal is created successfully ***")
            # time.sleep(5)
        # Transmittal Type-GCD/RFI/TRA -- END--------------------------

        # Execute the check_doc_properties method after the success message is displayed
        self.dp.check_doc_properties(docTitles, trasubject, self.path)
        logger_setup.logger.info("*** Created TRA  is successfully validated ***")
        logger_setup.logger.info("*** End of TRA creation test case ***")
