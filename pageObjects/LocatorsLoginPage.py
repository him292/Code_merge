from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    textbox_username_xpath = "//input[@placeholder='Email or username']"
    textbox_password_xpath = "//input[@placeholder='Password']"
    button_login_xpath = "//input[@type='submit']"
    checkbox_rememberme_xpath = "//div[@class='field remember-me']//div[@class='remember-me uwa-checkbox-content uwa-toggle-content uwa-input-content uwa-icon']"
    link_iamnot_xpath = "//a[contains(.,'I am not')]"
    button_profile_xpath = "//div[@class='profile-picture']"
    button_logout_xpath = "//span[contains(text(),'Log out')]"
    switchUser_reset_xpath = "//a[contains(.,'I am not')]"
    maximize_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-full']"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    # constructer to initialise driver
    def __init__(self, driver):
        self.driver = driver

    # # logger = LogGen.loggen()

    # Action Methods of LoginPage
    def setUserName(self, username):
        try:
            try:
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.link_iamnot_xpath))).click()

                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).clear()
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).send_keys(username)
            except:
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).clear()
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).send_keys(username)
            # logger_setup.logger.info(username + "** username is entered **")
        except Exception as e:
            raise e

    def setPassword(self, password):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.textbox_password_xpath))).clear()
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.textbox_password_xpath))).send_keys(password)
        # logger_setup.logger.info("** Password is entered **")

    def clickLogin(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.button_login_xpath))).click()
        # logger_setup.logger.info("** Clicked on login **")

    def uncheckRememberMe(self):
        self.driver.find_element(By.XPATH, self.checkbox_rememberme_xpath).click()
        logger_setup.logger.info("** Clicked on rememberMe **")
    def clickIAmNot(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.link_iamnot_xpath))).click()
        logger_setup.logger.info("** Clicked on IAmNot **")

    def clickProfile(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.button_profile_xpath))).click()
        # logger_setup.logger.info("** Clicked on Profile **")

    def clickLogout(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.button_logout_xpath))).click()
        logger_setup.logger.info("** Clicked on Logout **")

    def switchUser(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, self.switchUser_reset_xpath))).click()
