import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from pageObjects.Locators import LoginPage, DashboardAndTabs
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig


class Test_Dashboard_selection:
    baseURL = ReadConfig.getURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    widget_name = 'Document Register'
    # widget_name = 'Workflow Management'
    path = ".//TestData/DataManager.xlsx"

    logger = LogGen.loggen()

    def test_dashboard_selection(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = LoginPage(self.driver)
        time.sleep(5)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        time.sleep(10)
        dashboard = "GENERIC Dashboard"
        widget_name = 'Document Register'

        time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[@class='topbar-app-name']")))
            self.driver.find_element(By.XPATH,
                                     "//span[contains(@class,'topbar-app-name') and text()='" + dashboard + "']")
            # "//span[@title='" + self.dashboard_name + "']")
            time.sleep(5)
            try:
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            except:
                pass
        except:
            try:
                # click on Dashboards and cockpit list menu
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[@class='wp-panel-button fonticon fonticon-menu new-dashboard-menu-open-btn inactive']"))).click()
                # self.logger.info("** clicked on Dashboard and cockpit list menu **")
                try:
                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item']//p[@class='dashboard-menu-list-item-text-title' and text()='" + dashboard + "']"))).click()
                    self.logger.info("** clicked on Dashboard **")
                except Exception as e:
                    self.logger.info("** Fail to click on Dashboard **")
                    raise e
            except:
                try:
                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item-text-with-description']/p[contains(@class, 'dashboard-menu-list-item-text-title') and text()='" + dashboard + "']"))).click()
                    # self.logger.info("** ** clicked on Dashboard ** **")
                    WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(
                        (By.XPATH,
                         "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))
                except Exception as e:
                    raise e

            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))

        self.dt = DashboardAndTabs(self.driver)
        time.sleep(5)
        self.dt.clickdocumentmgtab()
        time.sleep(5)
        self.logger.info("*** Ended Navigate Document Management tab test ***")
