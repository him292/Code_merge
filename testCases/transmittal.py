import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardAndTabs, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import XLUtils


class Test_Transmittal:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    path = ".//TestData//DataManager.xlsx"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    logger = LogGen.loggen()

    def test_create_Transmittal(self, setup):
        self.dashboard = XLUtils.readData(self.path, "Inputs", 2, 1)
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

        traSelect = XLUtils.readData(self.path, 'transmittal', 3, 4)
        tratypeSelect = XLUtils.readData(self.path, 'transmittal', 3, 8)
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
        tra_category = XLUtils.readData(self.path, 'transmittal', 3, 20)
        tra_letter_ini = XLUtils.readData(self.path, 'transmittal', 2, 21)
        tra_letter_add = XLUtils.readData(self.path, 'transmittal', 2, 22)

        time.sleep(5)

        self.dt.dashboardselection(self.dashboard)
        time.sleep(3)

        self.dt.clickdocumentmgtab()
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
        time.sleep(5)

        self.tra.create_transmittal_button()
        time.sleep(5)

        # Transmittal Type-GCD -- START=======================================================
        # self.tra.traType_gcd(tratypeSelect)
        # time.sleep(5)
        # # self.tra.tra_toUser(to_username)
        # # time.sleep(10)
        # #
        # # self.tra.tra_ccUser(cc_username)
        # # time.sleep(10)
        #
        # self.tra.traResponseRequired(traresponse_rqd)
        # time.sleep(3)
        #
        # self.tra.traResponseDatePicker()
        # time.sleep(3)
        #
        # self.tra.tra_Subject(trasubject)
        # time.sleep(5)
        #
        # self.tra.tra_Message(traMessage)
        # time.sleep(3)
        # Transmittal Type-GCD -- END--------------------------

        # Tranmittal category = OTHER START========================================================
        # self.tra.traType_transmittal(tratypeSelect)
        # time.sleep(5)
        # self.tra.tra_toUser(to_username)
        # time.sleep(10)
        # self.tra.tra_ccUser(cc_username)
        # time.sleep(10)
        # self.tra.traReason(tra_reason)
        # time.sleep(3)
        # self.tra.traResponseRequired(traresponse_rqd)
        # time.sleep(1)
        # self.tra.traResponseDatePicker()
        # time.sleep(1)
        # self.tra.tra_Subject(trasubject)
        # time.sleep(5)
        # # ==================================== for catogory = other than LETTER
        # self.tra.tra_category_other(tra_category)
        # time.sleep(3)
        # # ==================================== for catogory = other than LETTER
        # self.tra.tra_contract(tra_contract)
        # time.sleep(3)
        #
        # self.tra.tra_wo(tra_wo)
        # time.sleep(3)
        #
        # self.tra.tra_discipline(disciplines)
        # time.sleep(3)
        #
        # self.tra.tra_Message(traMessage)
        # time.sleep(3)
        #
        # # Tranmittal category = OTHER END========================================================
        #
        # # Tranmittal category = LETTER START========================================================
        #
        # self.tra.traType_transmittal(tratypeSelect)
        # time.sleep(5)
        # self.tra.tra_toUser(to_username)
        # time.sleep(10)
        # # self.iframe.tra_ccUser(cc_username)
        # # time.sleep(10)
        # self.tra.traReason(tra_reason)
        # time.sleep(3)
        # self.tra.traResponseRequired(traresponse_rqd)
        # time.sleep(3)
        # self.tra.traResponseDatePicker()
        # time.sleep(3)
        # self.tra.tra_Subject(trasubject)
        # time.sleep(5)
        # ==================================== for catogory = Letter
        # below function is to for Type=TRA with Letter as category
        # self.tra.tra_category_ltr(tra_category)
        # time.sleep(3)
        # # ==================================== for catogory = Letter
        # self.tra.tra_contract(tra_contract)
        # time.sleep(3)
        #
        # self.tra.tra_wo(tra_wo)
        # time.sleep(3)
        #
        # self.tra.tra_discipline(disciplines)
        # time.sleep(3)
        #
        # # below will be execute when TR Categoty=Letter is selected
        # self.tra.ltr_initiator(tra_letter_ini)
        # time.sleep(3)
        #
        # self.tra.ltr_addressee(tra_letter_add)
        # time.sleep(3)
        #
        # self.tra.tra_Message(traMessage)
        # time.sleep(3)
        # Tranmittal category = LETTER END========================================================

        # Transmittal Type-Transmittal ----------------------------------------------------------- END
        #
        # Transmittal Type-RFI ------------------------------------------------------------------- -- START

        self.tra.traType_rfi(tratypeSelect)
        time.sleep(5)
        #
        self.tra.tra_toUser(to_username)
        time.sleep(10)

        # self.tra.tra_ccUser(cc_username)
        # time.sleep(10)
        #
        # self.tra.traResponseRequired(traresponse_rqd)
        # time.sleep(3)
        # # # # #
        # self.tra.traResponseDatePicker()
        # time.sleep(3)
        #
        self.tra.tra_Subject(trasubject)
        time.sleep(5)

        self.tra.rfi_assetCode(tra_asset)
        time.sleep(3)

        self.tra.tra_contract(tra_contract)
        time.sleep(3)
        # #
        self.tra.tra_wo(tra_wo)
        time.sleep(3)

        self.tra.rfi_stage(tra_stage)
        time.sleep(3)
        #
        self.tra.tra_discipline(disciplines)
        time.sleep(3)
        #
        self.tra.rfi_design(tra_design)
        time.sleep(3)

        self.tra.rfi_info_requested(tra_info)
        time.sleep(3)

        # # traMessage = ExcelUtils.readData(self.path, 'transmittal', 10, 7)
        self.tra.tra_Message(traMessage)
        time.sleep(3)

        # Transmittal Type-RFI ---------------------------------------------------------------------- END
        # passing the docTitle so that the code can check the docProperties using the title of the document
        docTitles = XLUtils.readData(self.path, 'transmittal', 2, 4)
        self.tra.tra_send(docTitles)
        time.sleep(10)
