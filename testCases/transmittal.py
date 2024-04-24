import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardTabs, iframes, regDocument_properties, transmittal_reply, Create_Transmittal
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from utilities import ExcelUtils


class Test_Transmittal:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    # widget_name = 'Workflow Management'
    # path = ".//TestData/LoginDataSheet.xlsx"
    path = "D://My Projects//Selenium//TestFramework//TestData//LoginDataSheet.xlsx"
    # docTitles = ["02-DAH-LAN-3DM-245004", "02-ABI-BMN-3DM-000011"]
    docTitles = "02-CH2-STR-MDL-900123"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    logger = LogGen.loggen()

    def test_create_Transmittal(self, setup):
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

        traSelect = ExcelUtils.readData(self.path, 'transmittal', 3, 4)
        tratypeSelect = ExcelUtils.readData(self.path, 'transmittal', 2, 8)
        to_username = ExcelUtils.readData(self.path, 'transmittal', 2, 5)
        cc_username = ExcelUtils.readData(self.path, 'transmittal', 3, 5)
        traresponse_rqd = ExcelUtils.readData(self.path, 'transmittal', 2, 10)
        trasubject = ExcelUtils.readData(self.path, 'transmittal', 2, 11)
        tra_asset = ExcelUtils.readData(self.path, 'transmittal', 2, 12)
        tra_contract = ExcelUtils.readData(self.path, 'transmittal', 2, 13)
        tra_wo = ExcelUtils.readData(self.path, 'transmittal', 2, 14)
        tra_stage = ExcelUtils.readData(self.path, 'transmittal', 2, 15)
        disciplines = ExcelUtils.readData(self.path, 'transmittal', 2, 16)
        tra_design = ExcelUtils.readData(self.path, 'transmittal', 2, 17)
        tra_info = ExcelUtils.readData(self.path, 'transmittal', 2, 18)
        traMessage = ExcelUtils.readData(self.path, 'transmittal', 2, 19)

        self.logger.info("*** Starting Dashboard Selection test ***")

        time.sleep(5)

        self.dt.dashboard_selection(dashboard)
        time.sleep(3)

        self.dt.clickdocumentmgtab()
        time.sleep(10)
        self.logger.info("** Doc Mngmt Tab selected **")

        # self.lp.click_menu_dropdown(self.widget_name)
        # time.sleep(5)

        self.iframe.navigate_to_tab_registered_document()
        time.sleep(10)

        # self.dp.reg_rows_filter()
        # time.sleep(10)

        docTitles = ExcelUtils.readData(self.path, 'transmittal', 2, 4)
        # for docTitle in docTitles:
        self.iframe.select_a_document(docTitles)
        time.sleep(5)

        self.tra.create_transmittal_button()
        time.sleep(5)

        # Transmittal Type-GCD -- START=======================================================
        self.tra.traType_gcd()
        time.sleep(5)
        self.tra.tra_toUser()
        time.sleep(10)

        # self.tra.tra_ccUser()
        # time.sleep(10)

        self.tra.traReason()
        self.tra.traResponseRequired()
        time.sleep(3)

        self.tra.traResponseDatePicker()
        time.sleep(3)

        self.tra.tra_Subject(trasubject)
        time.sleep(5)

        self.tra.tra_Message()
        time.sleep(3)
        # Transmittal Type-GCD -- END--------------------------

        # Tranmittal category = OTHER START========================================================
        self.tra.traType_transmittal()
        time.sleep(5)
        self.tra.tra_toUser()
        time.sleep(10)
        # self.iframe.tra_ccUser()
        # time.sleep(10)
        self.tra.traReason()
        time.sleep(3)
        self.tra.traResponseRequired()
        # time.sleep(3)
        # self.iframe.traResponseDatePicker()
        # time.sleep(3)
        self.tra.tra_Subject(trasubject)
        time.sleep(5)
        # ==================================== for catogory = other
        catVal = "MeetingMinutes"
        self.tra.tra_category_other(catVal)
        time.sleep(3)
        # ==================================== for catogory = other
        self.tra.tra_contract(tra_contract)
        time.sleep(3)

        self.tra.tra_wo(tra_wo)
        time.sleep(3)

        val = ["AVC - Audio Visual", "ARC - Architectural"]
        self.tra.tra_discipline(val)
        time.sleep(3)

        self.tra.tra_Message()
        time.sleep(3)

        # Tranmittal category = OTHER END========================================================

        # Tranmittal category = LETTER START========================================================

        self.tra.traType_transmittal()
        time.sleep(5)
        self.tra.tra_toUser()
        time.sleep(10)
        # self.iframe.tra_ccUser()
        # time.sleep(10)
        self.tra.traReason()
        time.sleep(3)
        self.tra.traResponseRequired()
        time.sleep(3)
        self.tra.traResponseDatePicker()
        time.sleep(3)
        self.tra.tra_Subject(trasubject)
        time.sleep(5)
        # ==================================== for catogory = Letter
        # below function is to for Type=TRA with Letter as category
        catVal_ltr = "Letter"
        self.tra.tra_category_ltr(catVal_ltr)
        time.sleep(3)
        # ==================================== for catogory = Letter
        self.tra.tra_contract(tra_contract)
        time.sleep(3)

        self.tra.tra_wo(tra_wo)
        time.sleep(3)
        val = ["AVC - Audio Visual", "ARC - Architectural"]
        self.tra.tra_discipline(val)
        time.sleep(3)
        # below will be execute when TR Categoty=Letter is selected
        ltr_ini_val = ["AECOM-Khaled Ismail", "ALMABANI-Etienne Chehwan"]
        self.tra.ltr_initiator(ltr_ini_val)
        time.sleep(3)

        ltr_adr_val = ["AECOM-Werner Van Straaten", "AECOM-Khaled Ismail"]
        self.tra.ltr_addressee(ltr_adr_val)
        time.sleep(3)

        self.tra.tra_Message()
        time.sleep(3)
        # Tranmittal category = LETTER END========================================================

        # Transmittal Type-Transmittal ----------------------------------------------------------- END
        #
        # Transmittal Type-RFI ------------------------------------------------------------------- -- START

        ExcelUtils.readData(self.path, 'transmittal', 2, 7)
        self.tra.traType_rfi(tratypeSelect)
        time.sleep(5)
        #
        # # to_username = ExcelUtils.readData(self.path, 'transmittal', 11, 7)
        self.tra.tra_toUser()
        time.sleep(10)
        # # cc_username = ExcelUtils.readData(self.path, 'transmittal', 12, 7)
        # self.tra.tra_ccUser()
        # time.sleep(10)
        # self.tra.traResponseRequired()
        # time.sleep(3)
        # # #
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
        val = ["AVC - Audio Visual", "ARC - Architectural"]
        self.tra.tra_discipline(val)
        time.sleep(3)
        #
        self.tra.rfi_design(tra_design)
        time.sleep(3)

        self.tra.rfi_info_requested(tra_info)
        time.sleep(3)

        # # traMessage = ExcelUtils.readData(self.path, 'transmittal', 10, 7)
        self.tra.tra_Message()
        time.sleep(3)

        # Transmittal Type-RFI ---------------------------------------------------------------------- END

        docTitles = ExcelUtils.readData(self.path, 'transmittal', 2, 4)
        self.tra.tra_send(docTitles)
        time.sleep(10)
