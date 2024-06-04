import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from utilities import XLUtils

from utilities.customLogger import LogGen
from selenium.webdriver.support.ui import Select


class LoginPage:
    textbox_username_xpath = "//input[@placeholder='Email or username']"
    textbox_password_xpath = "//input[@placeholder='Password']"
    button_login_xpath = "//input[@type='submit']"
    checkbox_rememberme_xpath = "//div[@class='field remember-me']//div[@class='remember-me uwa-checkbox-content uwa-toggle-content uwa-input-content uwa-icon']"
    link_iamnot_xpath = "//a[contains(.,'I am not')]"
    button_profile_xpath = "//div[@class='profile-picture']"
    button_logout_xpath = "//span[contains(text(),'Log out')]"

#constructer to initialise driver
    def __init__(self,driver):
        self.driver = driver

#Action Methods of LoginPage
    def setUserName(self,username):
        try:
            try:
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.link_iamnot_xpath))).click()

                # self.driver.find_element(By.XPATH,'link_iamnot_xpath')
                #
                # ActionChains(self.driver).move_to_element(self.link_iamnot_xpath).click(self.link_iamnot_xpath).perform()

                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH,self.textbox_username_xpath))).clear()
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).send_keys(username)
            except:
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).clear()
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.textbox_username_xpath))).send_keys(username)

        except Exception as e:
            raise e


    def setPassword(self,password):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.textbox_password_xpath))).clear()
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.textbox_password_xpath))).send_keys(password)

    def clickLogin(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.button_login_xpath))).click()

    def uncheckRememberMe(self):
        self.driver.find_element(By.XPATH,self.checkbox_rememberme_xpath).click()

    def clickIAmNot(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_iamnot_xpath))).click()

    def clickProfile(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.button_profile_xpath))).click()

    def clickLogout(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.button_logout_xpath))).click()

class DashboardAndTabs:  # all dashboard tabs locators
    link_projectinsights_tab_xpath = "//span[contains(@class, 'title') and text() = 'Project Insights']"
    link_documentmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Document Management']"
    link_workflowmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Workflow Management']"
    link_mailmanagement_tab_xpath = "//span[contains(@class, 'title') and text() = 'Mail Management']"
    link_alltasksview_tab_xpath = "//span[contains(@class, 'title') and text() = 'All Tasks View']"
    title_documentreg_xpath = "//div[contains(@class, 'moduleHeader__title') and text() = 'Document Register']"
    #menu_dropdown_xpath_1 = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@id='m_9sMywGd0g06qZr2-U046']//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"
    #menu_dropdown_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='Document Register']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"
    maximize_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-full']"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"

    # constructer to initialise driver
    def __init__(self, driver):
        self.driver = driver

    #logger = LogGen.loggen()

#Action Methods of DashboardTabs
    def dashboardselection(self,dashboard):
        try:
            WebDriverWait(self.driver, 300).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[@class='topbar-app-name']")))
            WebDriverWait(self.driver, 300).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//span[contains(@class,'topbar-app-name') and text()='" + dashboard + "']")))
            #self.logger.info("** Dashboard is selected **")
        except NoSuchElementException:
            try:
                # click on Dashboards and cockpit list menu
                WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[@class='wp-panel-button fonticon fonticon-menu new-dashboard-menu-open-btn inactive']"))).click()
                #self.logger.info("** clicked on Dashboard and cockpit list menu **")
                try:
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//div[@class='dashboard-menu-list-item-text']/p[text()='" + dashboard + "']"))).click()
                    #self.logger.info("** clicked on Dashboard **")

                except Exception as e:
                    #self.logger.info("** Fail to click on Dashboard **")
                    raise e
            except Exception as e:
                #self.logger.info("** Fail **")
                raise e

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']"))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//span[@class='fonticon fonticon-close new-dashboard-menu-close-btn']")))

    def clickprojectinsightstab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_projectinsights_tab_xpath))).click()
    def clickdocumentmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_documentmanagement_tab_xpath))).click()
    def clickworkflowmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_workflowmanagement_tab_xpath))).click()
    def clickmailmgtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_mailmanagement_tab_xpath))).click()
    def clickalltasksviewtab(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,self.link_alltasksview_tab_xpath))).click()

    def click_menu_dropdown(self,widget_name):
        WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable']"))).click()
        time.sleep(3)
    def close_menu_dropdown(self,widget_name):
        WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
            (By.XPATH,"//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable active']"))).click()
    def maximize_widget(self,widget_name):
        '''
        Method to maximise the widget
        '''
        try:
            maximize = (WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.maximize_xpath))))
            maximize.click()
            time.sleep(2)
            #self.logger.info("** widget is maximized **")
        except:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.restore_xpath)))
            #self.logger.info("** widget is already maximized **")
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

class documentRegisterAndWorkflow:  # all document register and workflow creation locators

    iframeNMDocumentCntrl_xpath = "//div[@id='7zAw5w30gCwH0QgEjm01']//iframe[@id='frame-9sMywGd0g06qZr2-U046']"
    tabDocumentUpload_xpath = "//a[contains(.,'Document Upload')]"
    tabTemporaryDocument_xpath = "//a[contains(.,'Temporary Document')]"
    tabRegisteredDocument_xpath = "//a[contains(.,'Registered Document')]"
    tabLegacyDocument_xpath = "//a[contains(.,'Legacy Document')]"
    select_files_xpath = "//div[@id='mass_upload']//div[contains(.,'Select File/s *')]//child::input[@id='input-19']"
    clear_file_path = "//button[@class='v-icon notranslate v-icon--link mdi mdi-close theme--light']"
    complete_upload = "//div[@role='progressbar']//i[contains(.,'100%')]"
    bt_inline_edit_du = "//button[@class='v-icon notranslate v-icon--link mdi mdi-pencil theme--light']"
    bt_mass_edit_du = "//div[@class='v-speed-dial v-speed-dial--bottom v-speed-dial--left v-speed-dial--direction-top']"
    bt_mass_edit_1 = "//button[@class='v-btn v-btn--is-elevated v-btn--fab v-btn--has-bg v-btn--round theme--dark v-size--small green']"
    mass_edit_form = "//div[@class='v-card__title']//span[contains(@class, 'headline') and text() = 'Mass Edit']"
    text_ms_title_field ="//label[text() = 'Title']/../input[@type='text']"
    drp_ms_wo_field = "//label[text() = 'Work Order/Service Order']/.."
    ms_wo_drp = "// div[@class='v-menu__content theme--light v-menu__content--fixed menuable__content__active']//div[@class='v-list v-select-list v-sheet theme--light theme--light']"
    drp_ms_status_field = "//label[text() = 'Status']/.."
    ms_status_drp = "// div[@class='v-menu__content theme--light v-menu__content--fixed menuable__content__active']"
    drp_ms_stage_field = "//label[text() = 'Stage']/.."
    ms_stage_drp = "// div[@class='v-menu__content theme--light v-menu__content--fixed menuable__content__active']"
    bt_update_all = "//span[contains(@class, 'v-btn__content') and text() = 'UPDATE ALL']"
    bt_test = "//button[@class='mb-2 v-btn v-btn--is-elevated v-btn--has-bg theme--dark v-size--default primary']/span[text()='TEST']"
    bt_save = "//button[@class='mb-2 v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default success']/span[text()='SAVE']"
    bt_plus_menu = "//i[@class='v-icon notranslate mdi mdi-plus theme--dark']"
    bt_create_workflow = "//div[@style='transition-delay: 0.2s;']//div[@class='v-responsive__content']"
    wf_template_search = "//div[(@class='fa fa-search search') and (@linked='routeTemplateOID')]"
    route_tmp_page = "//div[@class=' search-content-set-detail content-set-detail set-detail']"
    bt_route_ok = "//button[@id='id_in_app_ok' and text() = 'OK']"
    wf_title = "//input[@name='IMP_WFTitle']"
    bt_wf_create = "//div[starts-with(@id,'formdivision')]//following-sibling::div/button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus']"
    pg_route_mg = "//div[contains(@class,'moduleHeader__title') and text() = 'ENOVIA - Route Management - My Routes (1)']"
    iframerouteMg_xpath = "//div[@class='moduleWrapper']//iframe[starts-with(@id, 'frame-preview-')]"
    created_wf = "//div[@class='wux-layouts-datagridview-tweaker-container']/div[contains(text(), 'WF-')]"
    lnk_start_wf = "//div[@id='channel1']/div[@class='maturity-state-container']//a[contains(text(), 'Start')]"
    awaiting_approval_xpath = "//div[@id='channel1']/div[@class='maturity-state-container']//span[@class='rt-activity-state' and @title='Awaiting Approval']"



    # constructer to initialise diver
    def __init__(self, driver):
        self.driver = driver

    #logger = LogGen.loggen()

    def navigate_to_tab_document_upload(self):
        '''
                Method to navigate to the Document tab in Document Register widget
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tabDocumentUpload_xpath))).click()

        except Exception as e:
            raise e

    def navigate_to_tab_registered_document(self):
        '''
                Method to navigate to the Registered Document tab in Document Register widget
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tabRegisteredDocument_xpath))).click()

        except Exception as e:
            raise e

    def select_file(self,folder_path):
        '''
                Method to select files from local
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)

            # List all unique files in the folder
            file_paths = set(os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f)))

            # Find the file input field
            file_input = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                 (By.XPATH, self.select_files_xpath)))

            # Iterate over file paths and send each one individually
            for path in file_paths:
                file_input.send_keys(path + " ")
                #clear the file input filed
                WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH,self.clear_file_path))).click()


            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.complete_upload)))

        except Exception as e:
            raise e
    def store_file_names(self,path,folder_path):

        # Get a list of file names in the folder
        file_names = os.listdir(folder_path)

        # This will create a list of variables named file1, file2, file3, etc.
        variables = [file_name for file_name in file_names]
        #Write the values of the variables to the Excel file
        for i, data1 in enumerate(variables):
            substrings = data1.split("_")
            data = substrings[0]
            XLUtils.writeData(path, "Inputs", i+2, 8,data)

    def validate_reg_documents(self,docnames):
        try:
            # Locate the all rows in document table
            rows = WebDriverWait(self.driver, 50).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@id='regDocTable']//table/tr")))

            for docname in docnames:
                regDoc = WebDriverWait(self.driver, 50).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href, '#') and text() = '" + docname + "']")))
                self.driver.save_screenshot(
                    "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\DocReg_screenshots\\docregistered.png")
                docno = regDoc.text
                if regDoc.is_displayed():
                    print(f"'{docno}' is displayed")
                    # assert docno == expected_docno, f"Expected text '{expected_docno}' but found '{docno}'"
                    assert True
                else:
                    print(f"'{docno}' is not displayed")
                    # assert docno == expected_docno, f"Expected text '{expected_docno}' but found '{docno}'"
                    self.driver.save_screenshot(
                        "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\DocReg_screenshots\\docNotRegistered.png")
                    assert False

        except Exception as e:
            raise e

    def open_document_edit_form(self):
        '''
                Method to wait till completion of file upload
                '''
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
            (By.XPATH, self.complete_upload)))
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, self.bt_mass_edit_du))).click()
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, self.bt_mass_edit_1))).click()
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, self.mass_edit_form)))

    def update_document_title(self, title):
        try:
            ''' Entering text into title field '''
            title_field = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.text_ms_title_field)))
            title_field.click()
            time.sleep(2)
            title_field.send_keys(title)
        except Exception as e:
            raise e

    def update_document_workorder(self, wo_number):
        try:
            ''' selecting wo from dropdown '''
            ms_wo_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.drp_ms_wo_field)))
            ''' Clicking on dropdown '''
            ms_wo_selection.click()
            time.sleep(2)
            ''' Waiting till visibility of all options from dropdown '''
            wo_drp = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.ms_wo_drp)))

            ''' finding desired option from dropdown '''
            desired_wo = (wo_drp.find_element
                          (By.XPATH, "//div[contains(@class, 'v-list-item__title') and text() = '" + wo_number + "']"))
            ''' scrolling to desired option in dropdown '''
            ActionChains(self.driver).scroll_to_element(desired_wo).perform()
            desired_wo.click()
        except Exception as e:
            raise e

    def update_document_status(self, status):
        try:
            ''' selecting status from dropdown '''
            ms_wo_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.drp_ms_status_field)))
            ms_wo_selection.click()
            status_drp = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.ms_status_drp)))

            desired_status = (status_drp.find_element
                              (By.XPATH,
                               "// div[contains(@class , 'v-list-item__title') and text() = '" + status + "']"))
            ActionChains(self.driver).scroll_to_element(desired_status).perform()
            desired_status.click()
        except Exception as e:
            raise e

    def update_document_stage(self, stage):
        try:
            ''' selecting stage from dropdown '''
            ms_wo_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.drp_ms_stage_field)))
            ms_wo_selection.click()
            stage_drp = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.ms_stage_drp)))

            desired_stage = (stage_drp.find_element
                             (By.XPATH, "// div[contains(@class , 'v-list-item__title') and text() = '" + stage + "']"))
            ActionChains(self.driver).scroll_to_element(desired_stage).perform()
            desired_stage.click()
            time.sleep(3)
        except Exception as e:
            raise e

    def test_save_document(self):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_update_all))).click()

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_test))).click()

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_save))).click()
        except Exception as e:
            raise e

    def select_document(self, docname):
        try:
            # Locate the all rows in document table
            rows = WebDriverWait(self.driver, 50).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@id='regDocTable']//table/tr")))
            #self.logger.info("table is identified")

            checkbox = (rows.find_element(By.XPATH,
                                        "//a[contains(@href, '#') and text() = '" + docname + "']/../..//div[@class='v-input--selection-controls__ripple']"))
            #self.logger.info("Check box is identified")
            # Click on Checkbox
            ActionChains(self.driver).scroll_to_element(checkbox).perform()
            checkbox.click()
            #self.logger.info("Check box is selected")

        except Exception as e:
            raise e

    def click_on_create_wf(self):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_plus_menu))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_create_workflow))).click()
        except Exception as e:
            raise e
    def select_wf_route_template(self,wf_route_template):
        try:
            # select route template
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.wf_template_search))).click()
            # self.logger.info("Clicked on search")
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.route_tmp_page)))
            # self.logger.info("Route template page opened")
            try:
                template = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='wux-controls-responsivetileview-maincontent']//span[@class='searchItemSpan search_item_in_apps' and text() = '" + wf_route_template + "']")))
                template.click()
            except StaleElementReferenceException:
                template = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='wux-controls-responsivetileview-maincontent']//span[@class='searchItemSpan search_item_in_apps' and text() = '" + wf_route_template + "']")))
                template.click()
            # self.logger.info("Route template selected")

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_route_ok))).click()
            time.sleep(3)
        except Exception as e:
            raise e

    def create_wf(self, wf_title,reasonforissue):
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_WFReasonForIssue']/option[contains(text(), '" + reasonforissue + "')]"))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.wf_title))).send_keys(wf_title)
            WebDriverWait(self.driver, 40).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_wf_create))).click()

        except Exception as e:
            raise e

    def start_WF(self,path):
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframerouteMg_xpath)))
            self.driver.switch_to.frame(frame1)
            wf = WebDriverWait(self.driver, 60).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.created_wf)))
            wfname = wf.text

            # Store the WF name in excel input
            XLUtils.writeData(path, "Inputs", 2, 14, wfname)

            #self.logger.info("Created WF is displayed" + wfname)
            ActionChains(self.driver).double_click(wf).perform()
            try:
                lnk_start = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.lnk_start_wf)))
                time.sleep(3)
                lnk_start.click()
                time.sleep(10)
                #self.logger.info("Created WF is started")

            except Exception as e:
                raise e
        except Exception as e:
            raise e

    def validate_started_wf(self,expected_state):
        try:
            state = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.awaiting_approval_xpath)))
            current_state = state.text
            if current_state == expected_state:
                print("Workflow is started")
            else:
                print("Workflow is not started")
            self.driver.save_screenshot("D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\workflow\\workflow_started.png")
            time.sleep(3)

        except Exception as e:
            raise e


class worklow_mg:
    #iframe_wf_widget = "//div[@class='module dock-item wi-9uao55t0g06q-siHcm1W leaf-widget moduleEditable']//iframe[starts-with(@id, 'frame')]"
    iframe_wf_widget = "//div[contains(@class,'IMP_WorkFlowManagment/IMP_WorkFlowManagment')]//iframe[starts-with(@id, 'frame')]"
    txt_wf_count = "//label[contains(., 'Number of WFs ')]"
    filter_xpath = "//span[@class='fa fa-filter dropbtn']"
    filter1_selected = "//div[@attr-selected='true' and @attr='filter' and text()='Completed']"
    filter1_notselected = "//div[@attr-selected='false' and @attr='filter' and text()='Completed']"
    filter2_selected = "//div[@attr-selected='true' and @attr='expand' and text()='Owned By Me']"
    filter2_notselected = "//div[@attr-selected='false' and @attr='expand' and text()='Owned By Me']"
    create_swf_icon = "//span[@title='Create SubWorkFlow']"
    swf_creation_page = "//span[@class='floatingPanel_title']/span[text()='Create Sub WorkFlow']"
    swf_Title = "//input[@name='IMP_WFTitle']"
    swf_template_search = "//div[(@class='fa fa-search search') and (@linked='routeTemplateOID')]"
    route_tmp_page = "//div[@class=' search-content-set-detail content-set-detail set-detail']"
    bt_ok = "//button[@id='id_in_app_ok' and text() = 'OK']"
    content_search = "//div[(@class='fa fa-search search') and (@linked='contentList')]"
    content_page = "//div[@class=' search-content-set-detail content-set-detail set-detail']"
    doc_page = "//div[@class='wux-layouts-gridengine-scroller-container']"
    create_btn = "//div[starts-with(@id,'formdivision')]//following-sibling::div/button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus']"
    #pg_route_mg = "//div[@class='moduleHeader__title' and contains(text(), 'Route Management')]"
    iframerouteMg_xpath = "//div[@class='moduleWrapper']//iframe[starts-with(@id, 'frame-preview-')]"
    created_swf = "//div[@class='id-card-title-section']//span[contains(text(), 'SWF-')]"
    lnk_start_swf = "//div[@id='channel1']/div[@class='maturity-state-container']//a[contains(text(), 'Start')]"
    awaiting_comment_xpath = "//div[@id='channel1']/div[@class='maturity-state-container']//span[@class='rt-activity-state' and @title='Awaiting Comment']"
    create_cmt_icon = "//span[@title='Create Comment']"
    cmt_creation_page = "//span[@class='floatingPanel_title']/span[text()='Create Comment']"
    cmt_description = "//textarea[@name='description' and contains(@class,'form-control')]"

    # constructer to initialise diver
    def __init__(self, driver):
        self.driver = driver

    # logger = LogGen.loggen()

    def select_WF_filter(self,filter1,filter2):
        '''
                Method to select the filter to see appropriate workflows
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.txt_wf_count)))
            time.sleep(30)
            # click on filter
            filterbt1 = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.filter_xpath)))
            self.driver.execute_script("arguments[0].click();", filterbt1)
            time.sleep(3)

            try:
                # filter1 is already selected
                WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@attr-selected='true' and @attr='filter' and text()='" + filter1 + "']")))
                #self.logger.info("** Filter1 is already selected **")
                try:
                    # filter2 is already selected - select filter2
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH, "//div[@attr-selected='true' and @attr='expand' and text()='" + filter2 + "']"))).click()
                    #self.logger.info("** filter2 is already selected select filter2**")
                except:
                    # filter2 is not selected - select filter2
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH, "//div[@attr-selected='false' and @attr='expand' and text()='" + filter2 + "']"))).click()
                    #self.logger.info("** filter2 is not selected - select filter2 **")
                    time.sleep(10)

            except:
                # filter1 is not selected - select filter1
                filter1 = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//div[@attr-selected='false' and @attr='filter' and text()='" + filter1 + "']")))
                filter1.click()
                #self.logger.info("** filter1 is not selected - select filter1 **")
                # select filter
                filterbt2 = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.filter_xpath)))
                self.driver.execute_script("arguments[0].click();", filterbt2)
                #self.logger.info("** Filter1 is opened **")
                time.sleep(3)
                try:
                    # filter2 is already selected - select filter2
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH, self.filter2_selected))).click()
                    #self.logger.info("** filter2 is already selected - select filter2 **")
                except:
                    # filter2 is not selected - select filter2
                    WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH, self.filter2_notselected))).click()
                    #self.logger.info("** filter2 is not selected - select filter2 **")
        except Exception as e:
            raise e

    def select_Workflow(self, wf):
        '''
                Method to select the desired workflow
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//div[@title='" + wf + "']"))).click()
            time.sleep(10)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\subworkflow\\wf_selected.png")
        except Exception as e:
            raise e

    def select_inboxTask(self,assignee):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//tr[@type='Inbox Task']//div[@class='tddivcommon wrap' and @title='" + assignee + "']/ancestor::tr[@class='impgrid TRDetails expanded branch']"))).click()
        except Exception as e:
            raise e

    def click_on_create_swf(self):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,self.create_swf_icon))).click()
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,self.swf_creation_page)))
            time.sleep(5)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\subworkflow\\create_subworkflow_form.png")

        except Exception as e:
            raise e

    def select_swf_route_template(self,swf_route_template):
        try:
            # select route template
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.swf_template_search))).click()
            # self.logger.info("Clicked on search")
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.route_tmp_page)))
            # self.logger.info("Route template page opened")
            try:
                template = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='wux-controls-responsivetileview-maincontent']//span[@class='searchItemSpan search_item_in_apps' and text() = '" + swf_route_template + "']")))
                template.click()
            except StaleElementReferenceException:
                template = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='wux-controls-responsivetileview-maincontent']//span[@class='searchItemSpan search_item_in_apps' and text() = '" + swf_route_template + "']")))
                template.click()

            # self.logger.info("Route template selected")
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_ok))).click()
        except Exception as e:
            raise e

    def select_content_s_or_m(self,contents):
        try:
            # Click on content search
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.content_search))).click()

            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.content_page)))

            actions = ActionChains(self.driver)
            for doc in contents:
                # self.logger.info("** control key pressed **")
                content = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//span[@class='searchItemSpan' and text() = '" + doc + "']/ancestor::div[@class='wux-controls-responsivetileview-maincontent']")))
                content.click()
                # self.logger.info("** doc selected **")
                time.sleep(2)
                # Press and Hold the Ctrl key
                actions.key_down(Keys.CONTROL)
            # Release control key
            actions.key_up(Keys.CONTROL)
            # self.logger.info("** control key released **")
            actions.perform()
            # self.logger.info("content selected")
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_ok))).click()

        except Exception as e:
            raise e

    def select_content_all(self,doc1):
        try:
            # Click on content search
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            time.sleep(2)
            WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.content_search))).click()
            time.sleep(2)

            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.content_page)))
            try:
                content = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                    (By.XPATH, "//span[@class='searchItemSpan' and text() = '" + doc1 + "']/ancestor::div[@class='wux-controls-responsivetileview-maincontent']")))
                content.click()
            except StaleElementReferenceException:
                content = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                    (By.XPATH,
                     "//span[@class='searchItemSpan' and text() = '" + doc1 + "']/ancestor::div[@class='wux-controls-responsivetileview-maincontent']")))
                content.click()

            actions = ActionChains(self.driver)
            # Press and Hold the Ctrl key
            actions.key_down(Keys.CONTROL)
            time.sleep(2)
            actions.send_keys('a')
            time.sleep(1)
            actions.key_up('a')
            # Release the Ctrl key
            actions.key_up(Keys.CONTROL)
            # self.logger.info("** control key released **")
            actions.perform()
            # self.logger.info("** action performed **")
            time.sleep(2)
            # self.logger.info("content selected")
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.bt_ok))).click()

        except Exception as e:
            raise e

    def create_swf(self,swf_title):
        '''
                Method to create the subworkflow
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            title = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.swf_Title)))
            title.send_keys(swf_title)
            time.sleep(3)
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.create_btn)))
            WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.create_btn))).click()
            time.sleep(3)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\subworkflow\\swf_created.png")
        except Exception as e:
            raise e

    def start_SWF(self,path):
        try:
            # WebDriverWait(self.driver, 150).until(expected_conditions.visibility_of_element_located(
            #     (By.XPATH, self.pg_route_mg)))
            time.sleep(2)
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframerouteMg_xpath)))
            self.driver.switch_to.frame(frame1)

            swf = WebDriverWait(self.driver, 60).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.created_swf)))
            swfname = swf.text

            # Store the SWF name in excel input
            XLUtils.writeData(path, "Inputs", 3, 14, swfname)
            try:
                lnk_start = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.lnk_start_swf)))
                time.sleep(3)
                lnk_start.click()
                time.sleep(10)
                #self.logger.info("Created SWF is started")

            except Exception as e:
                raise e
        except Exception as e:
            raise e

    def validate_started_swf(self,expected_state):
        try:
            state = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.awaiting_comment_xpath)))
            current_state = state.text
            if current_state == expected_state:
                print("SubWorkflow is started")
            else:
                print("SubWorkflow is not started")
            self.driver.save_screenshot("D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\subworkflow\\Subworkflow_started.png")
            time.sleep(3)

        except Exception as e:
            raise e

    def expand_Workflow(self,wf):
        '''
                Method to expand the desired workflow
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@title='" + wf + "']")))
                #(By.XPATH, "//div[@title='" + wf + "']"))).click()
            WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//div[@title='" + wf + "']/parent::*/preceding-sibling::div[@class='expand']"))).click()
            time.sleep(10)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\wf_expanded.png")
        except Exception as e:
            raise e

    def select_Subworkflow(self,swf):
        '''
                Method to select the desired subworkflow
                '''
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_wf_widget)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//div[@title='" + swf + "']"))).click()
            time.sleep(10)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\swf_selected.png")
        except Exception as e:
            raise e

    def select_doc_under_task(self,assignee,doc):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//tr[@type='Inbox Task']//div[@class='tddivcommon wrap' and @title='" + assignee + "']/ancestor::tr[@class='impgrid TRDetails expanded branch']")))
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//tr[@type='Inbox Task']//div[@class='tddivcommon wrap' and @title='" + assignee + "']/ancestor::tr[@class='impgrid TRDetails expanded branch']/following-sibling::tr//div[@class='td-first-div wrap' and @title='" + doc + "']"))).click()
        except Exception as e:
            raise e

    def click_on_create_comment(self):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,self.create_cmt_icon))).click()
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,self.cmt_creation_page)))
            time.sleep(5)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\create_cmt_form.png")

        except Exception as e:
            raise e

    def create_cmt(self,desc,status):
        '''
                Method to create comment
                '''
        try:
            # self.driver.switch_to.default_content()
            # frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.iframe_wf_widget)))
            # self.driver.switch_to.frame(frame1)
            description = WebDriverWait(self.driver, 100).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.cmt_description)))
            description.send_keys(desc)
            select_status = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//select[@type='select' and @name='attribute[IMP_CRSInitialStatus]']/option[@value='" + status + "']")))
            select_status.click()
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.create_btn))).click()
            time.sleep(7)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\Comment_created.png")
        except Exception as e:
            raise e

    # def validate_doc_status(self,expected_statuses,assignee,doc):
    #     try:
    #         # status = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
    #         #     (By.XPATH, "//div[@class='tddivcommon wrap' and @title='D - Rejected']")))
    #         status = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
    #             (By.XPATH,
    #              "//tr[@type='Inbox Task']//div[@class='tddivcommon wrap' and @title='" + assignee + "']"
    #             "/ancestor::tr[@class='impgrid TRDetails expanded branch']"
    #             "/following-sibling::tr//div[@class='td-first-div wrap' and @title='" + doc + "']/ancestor::tr[@class='impgrid TRDetails expanded branch']//td[@class='td-common' and @name='IMP_WFReviewOutcome'")))
    #         current_status = status.text
    #         if current_status in expected_statuses:
    #             print("Doc Status is updated")
    #         else:
    #             print("Doc Status is not updated to any of the expected statuses: {', '.join(expected_statuses)}")
    #         self.driver.save_screenshot("D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\doc status.png")
    #         time.sleep(3)
    #
    #     except Exception as e:
    #         raise e

    # def validate_created_cmt(self,expected_state):
    #     try:
    #         state = WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located(
    #             (By.XPATH, self.awaiting_comment_xpath)))
    #         current_state = state.text
    #         if current_state == expected_state:
    #             print("SubWorkflow is started")
    #         else:
    #             print("SubWorkflow is not started")
    #         self.driver.save_screenshot("D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\subworkflow\\Subworkflow_started.png")
    #         time.sleep(3)
    #
    #     except Exception as e:
    #         raise e

class import_comments:
    export_crs_template = "//span[@title='Export CRS Template']"
    select_review_entity_wdw = "//div[@class='menu']//span[text()='Select Review Entity:']"
    choose_items = "//div[@class='menu']//span[text()='Choose items']"
    close_items = "//div[@style='display: inline-grid; grid-auto-flow: column;']"
    disp_list = "//div[@class='MultiSelectList']/label"
    save_btn = "//span[text()='Select Review Entity:']/../following-sibling::div/button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus']/span[text()='Save']"
    import_comments = "//span[@title='Import Comments']"
    import_comment_popup = "//div[@class='top']/div[@id='importcomment']"
    browse_crs_file = "//input[@id='inpSWFImportCRS']"
    clear_file_path = "//button[@class='v-icon notranslate v-icon--link mdi mdi-close theme--light']"


    # constructer to initialise diver
    def __init__(self, driver):
        self.driver = driver

    logger = LogGen.loggen()
    def click_on_export_CRS_Template(self):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.export_crs_template))).click()
            # self.logger.info("*** Clicked on export CRS template button ***")
            WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.select_review_entity_wdw)))
            # self.logger.info("*** select review entity window is opened ***")
            ch_item = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.choose_items)))
            ch_item.click()
        except Exception as e:
            raise e

    def select_disp(self, disciplines):
        try:
            # Locate the list of disciplines
            list = WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.disp_list)))

            for discipline in disciplines:
                discp = (list.find_element(By.XPATH,
                                           "//div[@class='MultiSelectList']//span[contains(text(), '" + discipline + "')]"))

                self.driver.execute_script("arguments[0].scrollIntoView();", discp)
                # select the checkbox
                checkbox = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='MultiSelectList']//span[contains(text(), '" + discipline + "')]/ancestor::label/input[@type='checkbox']")))
                checkbox.click()
                time.sleep(5)
                self.driver.save_screenshot(
                    "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\checkbox_selected.png")

        except Exception as e:
            raise e

    def click_on_save(self):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.close_items))).click()
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.save_btn))).click()
            time.sleep(1)
            self.driver.save_screenshot(
                "D:\\Git//test-automation\\feature\\Code_merge\\Screenshots\\Comment_Creation\\downloading_file.png")
            # self.logger.info("*** File is downloaded ***")
        except Exception as e:
            raise e

    def click_on_Import_Comments(self,crs_file_path):
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.import_comments))).click()
            self.logger.info("*** Clicked on Import comments button ***")
            WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.import_comment_popup)))
            self.logger.info("*** Import comments popup opened ***")

            file_input = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.browse_crs_file)))
            self.logger.info("*** Clicked on browse ***")
            file_input.send_keys(crs_file_path)
            self.logger.info("*** CRS file is selected ***")
        except Exception as e:
            raise e

class regDocument_properties:
    reg_rows_per_page_filter = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='50']"
    # reg_rows_per_page_filter = "//div[@class='v-data-footer__icons-after']//button[@class='v-btn v-btn--icon v-btn--round v-btn--text theme--light v-size--default']"
    reg_rows_per_page_all = "//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='All']"
    filter_xpath = "(//div[@class='v-input--selection-controls__ripple'])[3]"
    restore_xpath = "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//div[@class='widget-dd-menu dropdown-menu dropdown-menu-root dropdown dropdown-root']//child::span[@class='maximize-icon fonticon fonticon-resize-small']"
    all_rows_selected = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='All']"
    # document name panel - start
    doc_download_panel = "//div[@class='v-slide-group__content v-tabs-bar__content']//i[@class='v-icon notranslate v-icon--left mdi mdi-account-clock theme--light']"
    doc_transmittal_panel = "//div[@class='v-slide-group__content v-tabs-bar__content']//i[@class='v-icon notranslate v-icon--left mdi mdi-axis-arrow-lock theme--light']"
    doc_wf_panel = "//div[@class='v-slide-group__content v-tabs-bar__content']//i[@class='v-icon notranslate v-icon--left mdi mdi-sitemap theme--light']"
    doc_panel_close_button = "//div[@class='v-card__title']//span[@class='headline']/..//i[@class='v-icon notranslate mdi mdi-close theme--light']"
    # document name panel - end
    # document revision click - start
    doc_rev_click = "//a[contains(@href, '#') and text() = '02-NAP-MEP-MDL-000003']/../..//span[@style='cursor: pointer; color: blue;']"
    dev_rev_panel_close = "//button[@class='v-btn v-btn--text theme--light v-size--default secondary--text']//span[@class='v-btn__content' and text()='Close']"

    # document revision click - end

    def __init__(self, driver):
        self.lp = LoginPage(driver)
        self.driver = driver

    # logger = LogGen.loggen()

    def reg_rows_filter(self):

        #  Method to select the no of documents to be displayed within the reg doc tab
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_xpath)))
            # Wait for the filter button to be clickable
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.reg_rows_per_page_filter))).click()
            # logic to move the scroll bar to look for "All" filter
            doc_element = self.driver.find_element(By.XPATH, self.reg_rows_per_page_all)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.reg_rows_per_page_all))).click()

        except Exception as e:
            raise e

    def check_doc_properties(self, docTitle):
        # Method to select a document from reg doc tab and create WF
        try:
            #doc_link_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']"
            # checkbox_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']/../..//div[@class='v-input--selection-controls__ripple']"

            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.all_rows_selected)))

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '#') and text() = '" + docTitle + "']")
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#') and text() = '" + docTitle + "']"))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_download_panel))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_transmittal_panel))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_wf_panel))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_panel_close_button))).click()

        except Exception as e:
            raise e

    def check_doc_revision(self, docTitle):
        # Method to select a document from reg doc tab and create WF
        try:
            #doc_link_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']"
            #revision_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']/../..//span[@style='cursor: pointer; color: blue;']"

            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.all_rows_selected)))

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '#') and text() = '" + docTitle + "']")
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#') and text() = '" + docTitle + "']/../..//span[@style='cursor: pointer; color: blue;']"))).click()
            time.sleep(2)

            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.dev_rev_panel_close))).click()

        except Exception as e:
            raise e