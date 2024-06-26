import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from utilities.logger import logger_setup


class DashboardAndTabs:  # all dashboard tabs locators
    link_projectinsights_tab_xpath = "//span[contains(@class, 'title') and text() = 'Project Insights']"
    link_documentmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Document Management']"
    link_workflowmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Workflow Management']"
    link_mailmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Mail Management']"
    link_alltasksview_tab_xpath = "//span[contains(@class, 'title') and text() = 'All Tasks View']"
    title_documentreg_xpath = "//div[contains(@class, 'moduleHeader__title') and text() = 'Document Register']"
    # menu_dropdown_xpath_1 = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@id='m_9sMywGd0g06qZr2-U046']//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"
    # menu_dropdown_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='Document Register']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"
    maximize_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-full']"
    # restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::li[@name='leaveMaximize']"

    # constructer to initialise driver
    def __init__(self, driver):
        self.driver = driver

    # Action Methods of DashboardTabs
    def dashboardselection(self, dashboard):
        try:
            WebDriverWait(self.driver, 300).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[@class='topbar-app-name']")))
            WebDriverWait(self.driver, 300).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[contains(@class,'topbar-app-name') and text()='" + dashboard + "']")))
            logger_setup.logger.info("** Dashboard is selected **")
        except NoSuchElementException:
            try:
                # click on Dashboards and cockpit list menu
                WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[@class='wp-panel-button fonticon fonticon-menu new-dashboard-menu-open-btn inactive']"))).click()
                logger_setup.logger.info("** clicked on Dashboard and cockpit list menu **")
                try:
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item-text']/p[text()='" + dashboard + "']"))).click()
                    logger_setup.logger.info("** clicked on Dashboard **")

                except Exception as e:
                    logger_setup.logger.info("** Fail to click on Dashboard **")
                    raise e
            except Exception as e:
                logger_setup.logger.info("** Fail to click on cockpit **")
                raise e

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))

    def clickprojectinsightstab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_projectinsights_tab_xpath))).click()
        logger_setup.logger.info("** Navigate to Project Insights tab **")

    def clickdocumentmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_documentmanagement_tab_xpath))).click()
        logger_setup.logger.info("** Navigate to Document Management tab **")
    def clickworkflowmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_workflowmanagement_tab_xpath))).click()
        logger_setup.logger.info("** Navigate to Workflow Management tab **")

    def clickmailmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_mailmanagement_tab_xpath))).click()
        logger_setup.logger.info("** Navigate to Mail Management tab **")

    def clickalltasksviewtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_alltasksview_tab_xpath))).click()
        logger_setup.logger.info("** Navigate to all task view tab **")

    def click_menu_dropdown(self, widget_name):
        WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,
             "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"))).click()
        time.sleep(3)
        logger_setup.logger.info("** Clicked on menu dropdown **")

    def close_menu_dropdown(self, widget_name):
        WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,
             "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable active']"))).click()
        logger_setup.logger.info("** Menu Dropdown closed **")
    def maximize_widget(self, widget_name):
        '''
        Method to maximise the widget
        '''
        try:
            maximize = (WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.maximize_xpath))))
            maximize.click()
            time.sleep(2)
            logger_setup.logger.info("** widget is maximized **")
        except:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.restore_xpath)))
            logger_setup.logger.info("** widget is already maximized **")
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable active']"))).click()

    def restore_widget(self):
        '''
        Method to restore the widget
        '''
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.restore_xpath))).click()
        except:
            pass
