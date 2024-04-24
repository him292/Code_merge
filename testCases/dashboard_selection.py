import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from utilities import XLUtils

from pageObjects.Locators import LoginPage, DashboardTabs, iframes
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
#from pageObjects.Locators import LoginPage

class Test_003_Register_Document:
    path = ".//TestData//DataManager.xlsx"
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    #document_Reg = ReadConfig.getdocument_Reg()
    #dashboard_name = ReadConfig.getdashboard_name()
    #widget_name = ReadConfig.getdwidget_name()
    widget_name = 'Document Register'
    #widget_name = 'Workflow Management'
    #filepath = "C://Users//Lenovo//Desktop//sample_files//02-DAH-LAN-3DM-245003_A.pdf"

    logger = LogGen.loggen()

    def test_dashboard_selection(self,setup):

        self.folder_path = XLUtils.readData(self.path, "Sheet2",2 , 1)
        self.title = XLUtils.readData(self.path, "Sheet2", 3, 1)
        self.wo_number = XLUtils.readData(self.path, "Sheet2",4 , 1)
        self.status = XLUtils.readData(self.path, "Sheet2", 5, 1)
        self.stage = XLUtils.readData(self.path, "Sheet2", 6, 1)

        self.logger.info("*** login to the platform ***")
        self.driver = setup
        self.driver.get(self.baseURL)

        self.iframe = iframes(self.driver)

        self.lp = LoginPage(self.driver)
        time.sleep(5)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        self.logger.info("*** Login is successful ***")
        time.sleep(10)
        dashboard = "GENERIC Dashboard"
        #dashboard = self.dashboard_name

        self.logger.info("*** Starting Dashboard Selection test ***")

        time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[@class='topbar-app-name']")))
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH,"//span[contains(@class,'topbar-app-name') and text()='" + dashboard +"']")))
            self.logger.info("** Dashboard is selected **")
        except NoSuchElementException:
            try:
                # click on Dashboards and cockpit list menu
                WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                    (
                    By.XPATH, "//span[@class='wp-panel-button fonticon fonticon-menu new-dashboard-menu-open-btn inactive']"))).click()
                self.logger.info("** clicked on Dashboard and cockpit list menu **")
                try:
                    WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='dashboard-menu-list-item-text']/p[text()='" + dashboard + "']"))).click()
                    self.logger.info("** clicked on Dashboard **")

                except Exception as e:
                    self.logger.info("** Fail to click on Dashboard **")
                    raise e
            except Exception as e:
                self.logger.info("** Fail **")
                raise e

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))

    #def test_document_upload(self, setup):

        self.dt = DashboardTabs(self.driver)
        time.sleep(5)
        self.dt.clickworkflowmgtab()
        time.sleep(5)
        # self.dt.clickmailmgtab()
        # time.sleep(5)
        # self.dt.clickalltasksviewtab()
        # time.sleep(5)
        # self.dt.clickprojectinsightstab()
        # time.sleep(5)
        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.dt.click_menu_dropdown(self.widget_name)
        self.dt.maximize_widget()
        #
        # try:
        #     time.sleep(5)
        #     self.dt.maximize_widget()
        #     self.logger.info("** widget is maximized **")
        #     time.sleep(5)
        #     #self.dt.close_menu_dropdown(self.widget_name)
        #
        # except:
        #     self.dt.restore_widget()
        #     self.dt.click_menu_dropdown(self.widget_name)
        #     self.dt.maximize_widget()
        #     self.logger.info("** widget is restored then maximized **")
        #     time.sleep(5)

        self.iframe.navigate_to_tab_document_upload()
        self.logger.info("** Clicked on Document Upload tab **")

        time.sleep(5)
        #self.iframe.select_file(self.filepath)
        self.iframe.select_file(self.folder_path)
        time.sleep(5)
        self.logger.info("** file is uploaded 100% **")

        self.iframe.open_document_edit_form()
        self.logger.info("** Document mass edit form is opened **")
        self.iframe.update_document_title(self.title)
        self.logger.info("*** Title entered successfully ***")
        self.iframe.update_document_workorder(self.wo_number)
        self.logger.info("*** Work Order successfully selected***")
        self.iframe.update_document_status(self.status)
        self.logger.info("*** Status successfully selected***")
        self.iframe.update_document_stage(self.stage)
        self.logger.info("*** Stage successfully selected***")
        self.iframe.test_save_document()
        self.logger.info("*** Clicked on SAVE button ***")

        time.sleep(5)
        self.logger.info("** Document Successfully Registered **")

        self.logger.info("*** Ended Navigate Document Management tab test ***")

