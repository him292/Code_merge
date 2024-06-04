import time

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from utilities.logger import logger_setup

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pageObjects.LocatorsLoginPage import LoginPage
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl


class regDocument_properties:
    reg_rows_per_page_filter = "//div[@style='width: 100%; height: auto;']//div[@class='v-select__selections']//div[@class='v-select__selection v-select__selection--comma' and text()='50']"
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
    iframeNMDocumentCntrl_xpath = "//div[@id='7zAw5w30gCwH0QgEjm01']//iframe[@id='frame-9sMywGd0g06qZr2-U046']"
    get_tra_success_msg = "//div[contains(@class, 'alert-success') and contains(text(), 'Transmittal Created Successfully')]"
    get_tra_no_within_table = "//thead[@class='v-data-table-header']//th[@class='text-start sortable']/../../..//td[@class='text-start' and contains(text(), '-')]"

    # document revision click - end

    def __init__(self, driver):
        self.lp = LoginPage(driver)
        self.driver = driver

    # logger = LogGen.loggen()

    def reg_rows_filter(self):

        #  Method to select the no of documents to be displayed within the reg doc tab
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)

            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_xpath)))
            # Wait for the filter button to be clickable
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, self.reg_rows_per_page_filter))).click()
            # logic to move the scroll bar to look for "All" filter
            doc_element = self.driver.find_element(By.XPATH, self.reg_rows_per_page_all)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, self.reg_rows_per_page_all))).click()

        except Exception as e:
            raise e

    # below method currently used to get the TRA number when a TRA is created
    def check_doc_properties(self, docTitle, subject, file_path):
        # Method to click on the document and the switch btw tabs
        try:
            doc_link_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']"

            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.all_rows_selected)))

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, doc_link_xpath)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, doc_link_xpath))).click()
            time.sleep(2)
            # WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            #     (By.XPATH, self.doc_download_panel))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_transmittal_panel))).click()
            time.sleep(2)

            # Add condition to validate subject - TRA info - START
            # for now, I've taken the index value to validate the SUBJECT value in the xpath, later on we can
            # modify it based on requirements
            transmittal_subject = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH,
                                                                 "//thead[@class='v-data-table-header']//th[@class='text-start sortable']//span[text()='Subject']/../../../..//tr//td[@class='text-start' and text()][3]"))).text
            if transmittal_subject == subject:
                print("Subject matched")
                assert True
            else:
                print("Subject mismatched")
                assert False
            # Add condition to validate subject - TRA info - END

            tra_no_from_table = WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.get_tra_no_within_table)))
            tra_no_text = tra_no_from_table.text
            print("tra no is ", tra_no_text)

            # file_path = ".//TestData//DataManager.xlsx"

            # Load the existing workbook
            workbook = openpyxl.load_workbook(file_path)

            # Select the specific sheet by name
            sheet = workbook["transmittal"]

            # Assuming you have extracted the text value
            # extracted_text = "PMC-RFI-000006"

            # Write the extracted text to cell D3
            sheet.cell(row=3, column=4, value=tra_no_text)

            # Save the changes to the workbook
            workbook.save(file_path)

            # WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            #     (By.XPATH, self.doc_wf_panel))).click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.doc_panel_close_button))).click()

        except Exception as e:
            raise e

    def check_doc_revision(self, docTitle):
        # Method to click on the rev of the document and verify details
        try:
            doc_link_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']"
            revision_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']/../..//span[@style='cursor: pointer; color: blue;']"

            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.all_rows_selected)))

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, doc_link_xpath)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, revision_xpath))).click()
            time.sleep(2)

            # Wait for the revision panel to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.dev_rev_panel_close)))

            # Get the document link and revision text after clicking the revision
            doc_link_after_click = self.driver.find_element(By.XPATH, doc_link_xpath).text

            print(" doc link is", doc_link_after_click)

            # Validate if the document link and revision text match the expected values
            # expected_doc_link = "expected_link_value"
            # expected_revision = "expected_revision_value"

            if doc_link_after_click == docTitle:
                print("Document link match the expected values.")
                assert True
            else:
                print("Document link do not match the expected values.")
                assert False

            # Close the revision panel
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.dev_rev_panel_close))).click()

        except TimeoutException as te:
            print("Timeout waiting for elements:", te)
        except Exception as e:
            print("Error:", e)

    # this method is to handle the preference menu "already opened"

    # def click_menu_dropdown(self, widget_name):
    #     try:
    #         WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.restore_xpath)))
    #         WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
    #             (By.XPATH,
    #              "//div[contains(@class, 'moduleWrapper clearfix ifwe-tabview')]//div[@class='wp-tabview-panel']//child::div[contains(@class,'moduleHeader__title') and text()='" + widget_name + "']//following-sibling::div//child::span[@class='widget-menu-icon ifwe-action-icon fonticon fonticon-down-open clickable active']"))).click()
    #         # logger_setup.logger.info("** widget is already maximized **")
    #         time.sleep(5)
    #     except Exception as e:
    #         self.lp.maximize_widget()
    #         # logger_setup.logger.info("** widget is maximized **")
    #         time.sleep(5)
    #         raise e


class Create_Transmittal:
    iframeNMDocumentCntrl_xpath = "//div[@id='7zAw5w30gCwH0QgEjm01']//iframe[@id='frame-9sMywGd0g06qZr2-U046']"
    mail_management_iframe_xpath = "//div[@class='moduleWrapper']//iframe[@id='frame-9wOjNo70g06qNYY8Lm01']"
    plus_menu_button = "//i[@class='v-icon notranslate mdi mdi-plus theme--dark']"
    # create_workflow_button = "//button[@class='v-btn v-btn--is-elevated v-btn--fab v-btn--has-bg v-btn--round theme--dark v-size--small yellow']//div[contains(@style, 'Create%20Workflow')]"
    widget_name = 'Document Register'
    reg_rows_per_page_filter = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='50']"
    # reg_rows_per_page_filter = "//div[@class='v-data-footer__icons-after']//button[@class='v-btn v-btn--icon v-btn--round v-btn--text theme--light v-size--default']"
    reg_rows_per_page_all = "//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='All']"
    all_rows_selected = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='All']"

    # transmittal START -----------------
    create_transmittal_xpath = "//div[@style='transition-delay: 0.1s;']//div[@class='v-responsive__content']"
    # tra_type_gcd = "//select[@name='IMP_MailType']//option[@value='GCD']"
    # tra_type_trans = "//select[@name='IMP_MailType']//option[@value='TRA']"
    # tra_type_rfi = "//select[@name='IMP_MailType']//option[@value='RFI']"
    tra_to_list = "//div[@linked='IMP_ToList']"
    # tra_to_person_selection = "//span[@class='searchItemSpan search_item_in_apps' and text()='Himanshu Sharma']/../../../../..//div[@class='wux-controls-responsivetileview-checkbox']"
    # tra_to_person_selection = "//div[@class='wux-controls-abstract wux-controls-responsivetileview wux-ui-state-activated wux-ui-state-prehighlighted']//div[@class='wux-controls-highlightborder wux-ui-state-prehighlighted']"
    tra_person_ok_button = "//button[@id='id_in_app_ok']"
    tra_cc_list = "//div[@linked='IMP_CCList']"
    # tra_cc_person_selection = "//span[@class='searchItemSpan search_item_in_apps' and text()='Jayesh Panat']/../../../../..//div[@class='wux-controls-responsivetileview-checkbox']"
    tra_reason = "//select[@name='IMP_ReasonForIssue']"
    # tra_response = "//select[@name='IMP_MailResponseRequired']//option[@value='Yes']"
    tra_DatePicker = "//input[@id='calendar_IMP_MailResponseRequiredDate']"
    tra_subject = "//input[@name='IMP_Subject']"
    tra_category = "//select[@name='IMP_TRACategory']"
    tra_contract = "//select[@name='IMP_ContractCode']"
    tra_workorder = "//select[@name='IMP_Workorder']"
    tra_message = "//body[@aria-label='Editor, IMP_Message']//p"
    tra_send_button = "//div[@style='text-align: right; height: 70px; padding: 17.5px; background-color: rgb(241, 241, 241); border-bottom-left-radius: 6px; border-bottom-right-radius: 6px; border-top: 1px solid rgb(229, 229, 229);']//button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus' and text()='Send']"
    tra_success_msg = "//div[contains(@class, 'alert-success') and contains(text(), 'Transmittal Created Successfully')]"
    # --- for TRA
    tra_response_value = "//select[@name='IMP_ReasonForIssue']//option[@value='IFD']"
    # tra_category_value = "//select[@name='IMP_TRACategory']//option[@value='MeetingMinutes']"
    tra_letter_category = "//select[@name='IMP_TRACategory']//option[@value='Letter']"
    # tra_contract_value = "//select[@name='IMP_ContractCode']//option[@value='0000100113']"
    # tra_wo_value = "//select[@name='IMP_Workorder']//option[@value='025']"
    tra_discipline_field_click = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Discipline']/../..//div[@class='v-input__control']//div[@class='v-select__selections']"
    tra_ltr_ini_field_check = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Letter Initiator']/../..//div[@class='v-input__control']//div[@class='v-select__selections']"
    tra_ltr_adr_field_check = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Letter Addressee']/../..//div[@class='v-input__control']//div[@class='v-select__selections']"
    message_iframe_xpath = "//iframe[@class='cke_wysiwyg_frame cke_reset']"
    locate_mesg_field = "//section[@style='width: 98%; padding-top: 3px; padding-bottom: 3px;']//h5[@style='padding-left: 10px;' and text()='Message']"
    locate_category_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Transmittal Category']"
    locate_contract_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Contract']"
    locate_wo_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Work Order/Service Order']"
    locate_reason_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Reason For Issue']"
    locate_discipline_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Discipline']"
    locate_ltr_ini_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Letter Initiator']"
    locate_ltr_adr_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Letter Addressee']"
    disc_display_list = "//div[@class='v-list v-select-list v-sheet theme--light v-list--dense theme--light' and @role='listbox']"
    ltr_initiator_list = "//div[@class='v-menu__content theme--light menuable__content__active v-autocomplete__content']//div[@class='v-list v-select-list v-sheet theme--light v-list--dense theme--light' and @role='listbox']"
    ltr_addressee_list = "//div[@class='v-menu__content theme--light menuable__content__active v-autocomplete__content']//div[@class='v-list v-select-list v-sheet theme--light v-list--dense theme--light' and @role='listbox']"

    # transmittal END ------------------
    # RFI START----------------------------------
    # rfi_assetcode_value = "//select[@name='IMP_Reg02_AssetCodeLevel6']//option[@value = '012110']"
    locate_asset_code_field = "//div[contains(@style, 'font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;') and contains(text(), 'Asset Code')]"
    locate_response_code_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Response Required']"
    # rfi_stage_value = "//select[@name='IMP_StageCode']//option[@value='02A']"
    locate_stage_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Stage']"
    # rfi_design_value = "//select[@name='IMP_RFIDesignRelated']//option[@value='Yes']"
    locate_design_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Design Related']"
    rfi_info_value = "//textarea[@name='IMP_RFIInformationRequested']"
    locate_info_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Information Requested']"

    # constructor to initialise driver
    def __init__(self, driver):
        self.lp = LoginPage(driver)
        self.driver = driver
        self.dp = regDocument_properties(self.driver)

    # logger = LogGen.loggen()

    def create_transmittal_button(self):
        try:

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.plus_menu_button))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.create_transmittal_xpath))).click()
        except Exception as e:
            raise e

    # Transmittal Type-General Correspondence -- START
    def traType_gcd(self, type):
        try:
            try:
                # WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                #     (By.XPATH, self.tra_enterType))).send_keys(traType)
                tra_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, "//select[@name='IMP_MailType']//option[@value='" + type + "']")))
                tra_selection.click()
                # dropdown_element = Select(tra_selection)
                # dropdown_element.select_by_visible_text(traType)
            except:
                pass
        except Exception as e:
            raise e

    def traType_rfi(self, value):
        try:
            try:
                # WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                #     (By.XPATH, self.tra_enterType))).send_keys(traType)
                # tra_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                #     (By.XPATH, self.tra_type_rfi)))
                tra_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, "//select[@name='IMP_MailType']//option[@value='" + value + "']")))
                tra_selection.click()
                # dropdown_element = Select(tra_selection)
                # dropdown_element.select_by_visible_text(traType)
            except:
                pass
        except Exception as e:
            raise e

    def tra_toUser(self, user):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_to_list))).click()
            time.sleep(15)
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='wux-controls-abstract wux-controls-responsivetileview']//div[@class='wux-controls-responsivetileview-maincontent']//div[@class='wux-button-label-ellipsis-wrap wux-ui-is-rendered wux-controls-responsivetileview-description']//span[@class='searchItemSpan' and text()='" + user + "']"))).click()
            # logger_setup.logger.info("**** Person selected ")
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_person_ok_button))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    def tra_ccUser(self, user):
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_cc_list))).click()
            time.sleep(10)
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='wux-controls-abstract wux-controls-responsivetileview']//div[@class='wux-controls-responsivetileview-maincontent']//div[@class='wux-button-label-ellipsis-wrap wux-ui-is-rendered wux-controls-responsivetileview-description']//span[@class='searchItemSpan' and text()='" + user + "']"))).click()
            # logger_setup.logger.info("**** Template selected ")
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_person_ok_button))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    # below method is used when a TRA is created for the first time from Document Management
    def traResponseRequired(self, value, isMailFrame=False):
        try:
            self.driver.switch_to.default_content()
            if isMailFrame:
                frame_mail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.mail_management_iframe_xpath)))
                self.driver.switch_to.frame(frame_mail)
            else:
                # Add code to switch to another frame if needed
                pass

            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_MailResponseRequired']//option[@value='" + value + "']"))).click()
        except Exception as e:
            print(f"An error occurred: {e}")
            if not isMailFrame:
                try:
                    # Switch to mail frame if the initial switch failed
                    self.driver.switch_to.default_content()
                    doc_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                        (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
                    self.driver.switch_to.frame(doc_frame)

                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//select[@name='IMP_MailResponseRequired']//option[@value='" + value + "']"))).click()
                except Exception as e_inner:
                    print(f"Failed to switch to mail_frame or doc_frame or select option: {e_inner}")
                    raise e_inner
            else:
                raise e

    # below method is used when a TRA is forwarded/replied from Mail management
    def traResponseRequired_reply_fwd(self, value, isMailFrame=True):
        try:
            self.driver.switch_to.default_content()
            if isMailFrame:
                frame_mail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.mail_management_iframe_xpath)))
                self.driver.switch_to.frame(frame_mail)
            else:
                # Add code to switch to another frame if needed
                pass

            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_MailResponseRequired']//option[@value='" + value + "']"))).click()
        except Exception as e:
            print(f"An error occurred: {e}")
            if not isMailFrame:
                try:
                    # Switch to mail frame if the initial switch failed
                    self.driver.switch_to.default_content()
                    doc_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                        (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
                    self.driver.switch_to.frame(doc_frame)

                    WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH,
                         "//select[@name='IMP_MailResponseRequired']//option[@value='" + value + "']"))).click()
                except Exception as e_inner:
                    print(f"Failed to switch to mail_frame or doc_frame or select option: {e_inner}")
                    raise e_inner
            else:
                raise e

    def traResponseDatePicker(self):
        try:
            date_picker = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_DatePicker)))
            date_picker.click()
            time.sleep(1)

            date_picker.send_keys(Keys.ENTER)

        except Exception as e:
            raise e

    def tra_Subject(self, value):
        #  Method to input WF details in WF creation window
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.tra_subject))).send_keys(value)
            time.sleep(5)
        except Exception as e:
            raise e

    def tra_Message(self, msg):

        try:
            message_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_mesg_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", message_field)
            frame2 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@class='cke_contents cke_reset']//iframe[@class='cke_wysiwyg_frame cke_reset']")))
            self.driver.switch_to.frame(frame2)
            # logger_setup.logger.info("in frame 2")
            message = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "//html[@dir='ltr']//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")))
            # logger_setup.logger.info("in Message field")
            message.send_keys(msg)
            time.sleep(10)
        except Exception as e:
            raise e

    # Transmittal Type-General Correspondence -- END

    # Transmittal Type-TRANSMITTAL -- START
    def traType_transmittal(self, type):
        try:
            try:
                tra_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, "//select[@name='IMP_MailType']//option[@value='" + type + "']")))
                tra_selection.click()
            except:
                pass
        except Exception as e:
            raise e

    # Transmittal Type-TRANSMITTAL -- START

    # below method is used when a TRA is created for the first time from Doc Management
    def traReason(self, reason):
        try:
            self.driver.switch_to.default_content()
            doc_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(doc_frame)

            reason_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_reason_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", reason_field)
            reason_select = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_ReasonForIssue']//option[@value='" + reason + "']")))
            reason_select.click()
        except Exception as e_inner:
            print(f"Failed to switch to mail_frame or select reason: {e_inner}")
            raise e_inner

    # def traReason(self, reason, isCreateTRA=False):
    #     try:
    #         self.driver.switch_to.default_content()
    #         if isCreateTRA:
    #             mail_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                 (By.XPATH, self.mail_management_iframe_xpath)))
    #             self.driver.switch_to.frame(mail_frame)
    #         else:
    #             pass
    #
    #         reason_field = WebDriverWait(self.driver, 20).until(
    #             EC.presence_of_element_located((By.XPATH, self.locate_reason_field)))
    #         self.driver.execute_script("arguments[0].scrollIntoView(true);", reason_field)
    #         reason_select = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
    #             (By.XPATH, "//select[@name='IMP_ReasonForIssue']//option[@value='" + reason + "']")))
    #         reason_select.click()
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         if not isCreateTRA:
    #             try:
    #                 self.driver.switch_to.default_content()
    #                 doc_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                     (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
    #                 self.driver.switch_to.frame(doc_frame)
    #
    #                 reason_field = WebDriverWait(self.driver, 20).until(
    #                     EC.presence_of_element_located((By.XPATH, self.locate_reason_field)))
    #                 self.driver.execute_script("arguments[0].scrollIntoView(true);", reason_field)
    #                 reason_select = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
    #                     (By.XPATH, "//select[@name='IMP_ReasonForIssue']//option[@value='" + reason + "']")))
    #                 reason_select.click()
    #             except Exception as e_inner:
    #                 print(f"Failed to switch to mail_frame or select reason: {e_inner}")
    #                 raise e_inner
    #         raise e

    # below method is used when a TRA is forwarded/replied from Mail management
    def traReason_reply_fwd(self, reason, isCreateTRA=True):
        try:
            self.driver.switch_to.default_content()
            if isCreateTRA:
                mail_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, self.mail_management_iframe_xpath)))
                self.driver.switch_to.frame(mail_frame)
            else:
                pass

            reason_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_reason_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", reason_field)
            reason_select = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_ReasonForIssue']//option[@value='" + reason + "']")))
            reason_select.click()
        except Exception as e:
            print(f"An error occurred: {e}")
            if not isCreateTRA:
                try:
                    self.driver.switch_to.default_content()
                    doc_frame = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                        (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
                    self.driver.switch_to.frame(doc_frame)

                    reason_field = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, self.locate_reason_field)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", reason_field)
                    reason_select = WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                        (By.XPATH, "//select[@name='IMP_ReasonForIssue']//option[@value='" + reason + "']")))
                    reason_select.click()
                except Exception as e_inner:
                    print(f"Failed to switch to mail_frame or select reason: {e_inner}")
                    raise e_inner
            raise e

    def tra_category_other(self, category_val):

        try:
            category_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_category_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", category_field)

            category_other_select = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//select[@name='IMP_TRACategory']//option[@value='" + category_val + "']")))
            category_other_select.click()

        except Exception as e:
            raise e

    def tra_category_ltr(self, category_val):

        try:
            category_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_category_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", category_field)

            category_letter_select = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//select[@name='IMP_TRACategory']//option[@value='" + category_val + "']")))
            category_letter_select.click()

        except Exception as e:
            raise e

    def ltr_initiator(self, ltr_ini):
        try:
            # Convert to list if single value
            if not isinstance(ltr_ini, list):
                ltr_ini = [ltr_ini]

            for initiator in ltr_ini:
                try:
                    ltr_ini_field = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, self.locate_ltr_ini_field)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", ltr_ini_field)

                    ltr_ini_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.tra_ltr_ini_field_check)))
                    ltr_ini_select.click()

                    # Locate the list of initiators
                    WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
                        (By.XPATH, self.ltr_initiator_list)))

                    ltr_ini_value = str(initiator).strip()  # Ensure initiator is converted to a string
                    ltr_ini_link_xpath = f"//div[@class='v-list-item__title' and text()='{ltr_ini_value}']"
                    logger_setup.logger.info("path is %s", ltr_ini_link_xpath)

                    initiator_link_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, ltr_ini_link_xpath)))

                    # Scroll the element into view
                    ActionChains(self.driver).move_to_element(initiator_link_element).perform()

                    checkbox_xpath = "//div[@class='v-list-item__title' and text()='" + ltr_ini_value + "']/../..//div[@class='v-simple-checkbox']"
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()

                except Exception as e:
                    raise e

            # Close the initiator selection after all selections are made
            ini_click_event_xpath = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and contains(text(), 'Letter Initiator')]"
            ini_close_selection = self.driver.find_element(By.XPATH, ini_click_event_xpath)

            actions = ActionChains(self.driver)
            actions.click(ini_close_selection).perform()

        except Exception as e:
            raise e

    # def ltr_addressee(self, ltr_adr):
    #     try:
    #         try:
    #             ltr_adr_field = WebDriverWait(self.driver, 20).until(
    #                 EC.presence_of_element_located((By.XPATH, self.locate_ltr_adr_field)))
    #             self.driver.execute_script("arguments[0].scrollIntoView(true);", ltr_adr_field)
    #
    #             ltr_adr_select = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                 (By.XPATH, self.tra_ltr_adr_field_check)))
    #             ltr_adr_select.click()
    #
    #             # Wait for the list of addressees to be visible
    #             WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
    #                 (By.XPATH, self.ltr_addressee_list)))
    #
    #             ltr_add_value = str(ltr_adr).strip()  # Convert to string
    #             ltr_add_link_xpath = f"//div[@class='v-list-item__title' and text()='{ltr_add_value}']"
    #
    #             # Wait for the element to be clickable
    #             addressee_link_element = WebDriverWait(self.driver, 20).until(
    #                 EC.visibility_of_element_located((By.XPATH, ltr_add_link_xpath)))
    #
    #             # Scroll to the element before locating
    #             ActionChains(self.driver).move_to_element(addressee_link_element).perform()
    #
    #             checkbox_xpath = "//div[@class='v-list-item__title' and text()='" + ltr_add_value + "']/../..//div[@class='v-simple-checkbox']"
    #             WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()
    #
    #         except Exception as e:
    #             raise e
    #
    #         time.sleep(1)
    #         # Locate and click the close selection button
    #         adr_click_event_xpath = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and contains(text(), 'Letter Addressee')]"
    #         adr_close_selection = WebDriverWait(self.driver, 10).until(
    #             EC.element_to_be_clickable((By.XPATH, adr_click_event_xpath)))
    #
    #         actions = ActionChains(self.driver)
    #         actions.click(adr_close_selection).perform()
    #     except Exception as e:
    #         raise e

    def ltr_addressee(self, ltr_adr_list):
        try:
            ltr_adr_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_ltr_adr_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", ltr_adr_field)

            ltr_adr_select = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.tra_ltr_adr_field_check)))
            ltr_adr_select.click()

            # Wait for the list of addressees to be visible
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.ltr_addressee_list)))

            for ltr_adr in ltr_adr_list:
                ltr_add_value = str(ltr_adr).strip()
                logger_setup.logger.info("value is %s", ltr_add_value)
                ltr_add_link_xpath = f"//div[@class='v-list-item__title' and text()='{ltr_add_value}']"
                logger_setup.logger.info("path is %s", ltr_add_link_xpath)
                # addressee_link_element = WebDriverWait(self.driver, 20).until(
                #     EC.visibility_of_element_located((By.XPATH, ltr_add_link_xpath)))
                #
                # # Scroll the element into view
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", addressee_link_element)

                # Click the checkbox
                checkbox_xpath = "//div[@class='v-list-item__title' and text()='" + ltr_add_value + "']/../..//div[@class='v-simple-checkbox']"
                checkbox_element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                checkbox_element.click()

                logger_setup.logger.info(f"** {ltr_adr} is selected **")

            # Close the addressee selection after all selections are made
            adr_click_event_xpath = "//div[contains(text(), 'Letter Addressee') and @style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;']"
            adr_close_selection = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, adr_click_event_xpath)))
            adr_close_selection.click()

        except Exception as e:
            raise e

    # def ltr_addressee(self, ltr_adr):
    #     try:
    #         ltr_adr_field = WebDriverWait(self.driver, 20).until(
    #             EC.visibility_of_element_located((By.XPATH, self.locate_ltr_adr_field)))
    #         self.driver.execute_script("arguments[0].scrollIntoView(true);", ltr_adr_field)
    #
    #         ltr_adr_select = WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, self.tra_ltr_adr_field_check)))
    #         ltr_adr_select.click()
    #
    #         for value in ltr_adr:
    #             ltr_adr_link_xpath = f"//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='{value}']"
    #             checkbox_xpath = f"{ltr_adr_link_xpath}/../..//div[@class='v-input--selection-controls__input']"
    #             print("ltr add xpath ", ltr_adr_link_xpath)
    #             # Scroll the element into view
    #             doc_element = self.driver.find_element(By.XPATH, ltr_adr_link_xpath)
    #             ActionChains(self.driver).move_to_element(doc_element).perform()
    #
    #             WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()
    #
    #         time.sleep(1)
    #         adr_click_event_xpath = "//div[contains(text(), 'Letter Addressee')]"
    #         adr_close_selection = self.driver.find_element(By.XPATH, adr_click_event_xpath)
    #
    #         actions = ActionChains(self.driver)
    #         # Perform left-click on the element
    #         actions.click(adr_close_selection).perform()
    #     except Exception as e:
    #         print(f"Error occurred: {e}")
    #         raise e

    def tra_contract(self, value):

        try:
            message_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_contract_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", message_field)

            # contract_select = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.tra_contract_value)))
            contract_select = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//select[@name='IMP_ContractCode']//option[@value='" + value + "']")))
            contract_select.click()

        except Exception as e:
            raise e

    def tra_wo(self, value):

        try:
            message_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_wo_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", message_field)

            # wo_select = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.tra_wo_value)))
            wo_select = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//select[@name='IMP_Workorder']//option[@value='" + value + "']")))
            wo_select.click()

        except Exception as e:
            raise e

    def tra_discipline(self, discipline_values):
        try:
            # Convert to list if single value
            if not isinstance(discipline_values, list):
                discipline_values = [discipline_values]

            for discipline_value in discipline_values:
                try:
                    desc_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.locate_discipline_field)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", desc_field)

                    discipline_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.tra_discipline_field_click)))
                    discipline_select.click()

                    # Locate the list of disciplines
                    WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
                        (By.XPATH, self.disc_display_list)))

                    discipline = str(discipline_value).strip()  # Ensure discipline_value is converted to a string
                    discipline_link_xpath = f"//div[@class='v-list-item__title' and text()='{discipline}']"
                    discipline_link_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, discipline_link_xpath)))

                    # Scroll the element into view
                    ActionChains(self.driver).move_to_element(discipline_link_element).perform()

                    # Click the checkbox
                    checkbox_xpath = "//div[@class='v-list-item__title' and text()='" + discipline + "']/../..//div[@class='v-simple-checkbox']"
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()

                except Exception as e:
                    raise e

            # Close the discipline selection after all selections are made
            disc_click_event_xpath = "//div[contains(text(), 'Discipline') and @style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;']"
            discipline_close_selection = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, disc_click_event_xpath)))

            actions = ActionChains(self.driver)
            actions.click(discipline_close_selection).perform()

        except Exception as e:
            raise e

    # Transmittal Type-TRANSMITTAL -- END

    # Transmittal Type-RFI -- START
    # Transmittal Type-RFI -- END

    def tra_send(self):

        #  Method to input TRA details in TRA creation window
        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)

            send_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.tra_send_button)))
            send_button.click()

            # Wait for the success message to be displayed
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.tra_success_msg)))

            assert success_message.is_displayed(), "Success message not displayed after sending TRA"

            # time.sleep(10)
        except Exception as e:
            raise e

    # -------- Transmittal Management END--------------------------------------------

    # ----------------------------------- RFI attributes START-----------------------------
    def rfi_assetCode(self, value):
        try:
            # self.driver.switch_to.default_content()
            # frame_mail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.mail_management_iframe_xpath)))
            # self.driver.switch_to.frame(frame_mail)

            asset_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.locate_asset_code_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", asset_field)

            # Convert the integer value to a string before concatenating
            value_str = str(value)
            asset_value = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//select[@name='IMP_Reg02_AssetCodeLevel6']//option[@value = '" + value_str + "']")))
            asset_value.click()

        except Exception as e:
            print("Error:", e)
            raise e

    def rfi_stage(self, value):
        try:
            stage_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_stage_field)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", stage_field)

            # asset_value = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.rfi_stage_value)))
            stage_value = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//select[@name='IMP_StageCode']//option[@value= '" + value + "']")))
            stage_value.click()

        except Exception as e:
            raise e

    def rfi_design(self, value):
        #  Method to input WF details in WF creation window
        try:
            # WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            #     (By.XPATH, self.rfi_design_value))).click()
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, "//select[@name='IMP_RFIDesignRelated']//option[@value= '" + value + "']"))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    def rfi_info_requested(self, value):
        #  Method to input WF details in WF creation window
        try:
            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.rfi_info_value))).send_keys("Test Information")
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.rfi_info_value))).send_keys(value)
            time.sleep(5)
        except Exception as e:
            raise e

    # ----------------------------------- RFI attributes END -----------------------------

    # Verifying the TRANSMITAL & Replying to a transmittal - START ===========================================================


class transmittal_reply:
    mail_management_iframe_xpath = "//div[@class='moduleWrapper']//iframe[@id='frame-9wOjNo70g06qNYY8Lm01']"
    filter_button = "//div[@style='z-index: 999999; height: 35px; margin-bottom: 5px; width: 100%;']//span[@class='fa fa-filter dropbtn']"
    filter_value_outstanding = "//div[@id='myDropdown']//div[@value='Outstanding']"
    filter_value_NA = "//div[@id='myDropdown']//div[@value='NA']"
    filter_value_Sent = "//div[@id='myDropdown']//div[@value='OwnedByMe']"
    filter_value_Inbox = "//div[@id='myDropdown']//div[@value='AssignedToMe']"
    close_filter_window_event = "//div[@style='z-index: 999999; height: 35px; margin-bottom: 5px; width: 100%;']"
    tra_open_button = "//ul[@class='custom-menu']//li[@title='Open']//div[contains(text(), 'Open')]"
    mail_properties_label = "//div[@class='floatingPanel_Header']//span[@class='floatingPanel_title']//span[contains(text(), 'Mail Properties')]"
    reply_button_xpath = "//div[@style='text-align: right; height: 70px; padding: 17.5px; background-color: rgb(241, 241, 241); border-bottom-left-radius: 6px; border-bottom-right-radius: 6px; border-top: 1px solid rgb(229, 229, 229);']//button[@type='button' and text()='Reply']"
    tra_response = "//select[@name='IMP_MailResponseRequired']//option[@value='Yes']"
    locate_mesg_field = "//section[@style='width: 98%; padding-top: 3px; padding-bottom: 3px;']//h5[@style='padding-left: 10px;' and text()='Message']"
    tra_person_ok_button = "//button[@id='id_in_app_ok']"
    tra_cc_list = "//div[@linked='IMP_CCList']"
    tra_to_list = "//div[@linked='IMP_ToList']"
    forward_button_xpath = "//button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus' and contains(@style, 'background-color: rgb(54, 142, 196)') and contains(@style, 'border-color: rgb(54, 142, 196)') and text()='Forward']"
    tra_discipline_field_click = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Discipline']/../..//div[@class='v-input__control']//div[@class='v-select__selections']"
    locate_discipline_field = "//div[@style='font-size: 14px; top: 3px; position: relative; padding: 4px; text-overflow: ellipsis; overflow: hidden; height: 30px; color: rgb(119, 121, 124); font-weight: 700;' and text()='Discipline']"
    disc_display_list = "//div[@class='v-list v-select-list v-sheet theme--light v-list--dense theme--light' and @role='listbox']"
    tra_success_msg = "//div[contains(@class, 'alert-success') and contains(text(), 'Transmittal action Successful !')]"

    def __init__(self, driver):
        self.driver = driver

    # logger = LogGen.loggen()

    # Selecting and validating the selected filters
    def selecting_sent_filters(self):
        try:
            self.driver.switch_to.default_content()
            frame_mail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.mail_management_iframe_xpath)))
            self.driver.switch_to.frame(frame_mail)
            locate_filter = WebDriverWait(self.driver, 50).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_button)))
            locate_filter.click()
            time.sleep(1)

            out_filter = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_value_outstanding)))

            # # logger_setup.logger.info(" html info is %s", out_filter)

            # Check if the filter element is selected (active)
            out_filter_select = out_filter.get_attribute("attr-selected")
            if out_filter_select != 'true':
                out_filter.click()
            else:
                pass
            time.sleep(1)

            na_filter = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.filter_value_NA)))
            # Check if the filter element is selected (active)
            na_filter_select = na_filter.get_attribute("attr-selected")
            if na_filter_select != 'true':
                na_filter.click()
            else:
                pass
            time.sleep(1)

            sent_filter = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_value_Sent)))

            # Check if the filter element is selected (active)
            sent_filter_select = sent_filter.get_attribute("attr-selected")
            if sent_filter_select != 'true':
                sent_filter.click()
            else:
                pass
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.close_filter_window_event))).click()
            time.sleep(2)
        except Exception as e:
            raise e

    def validate_tra_and_click(self, traSelect):
        try:
            tra_doc_xpath = "//tr[@type='IMP_TransmittalTask']//div[@type='IMP_TransmittalTask']/div[@class='td-first-div wrap' and text()='" + traSelect + "']"

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, tra_doc_xpath)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, tra_doc_xpath))).click()

            # Right-click on the element
            ActionChains(self.driver).context_click(doc_element).perform()
            time.sleep(2)

            open_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.tra_open_button)))
            open_button.click()

        except Exception as e:
            raise e

    def scroll_tra_properties(self):
        try:
            scroll_to_status = "//div[@class='scetion']//div[@title='Status' and text()='Status :']"
            scroll_to_attachments = "//button[contains(text(), 'Document Attachments')]"

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.mail_properties_label)))
            time.sleep(2)
            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, scroll_to_status)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            time.sleep(3)

            doc_element = self.driver.find_element(By.XPATH, scroll_to_attachments)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            time.sleep(3)

        except Exception as e:
            raise e

    def click_reply_command(self):

        try:
            reply_command_xpath = "//div[@class='floatingPanel_Header']//span[@class='floatingPanel_title']//span[@class='fa fa-reply close']"

            reply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, reply_command_xpath)))
            reply_button.click()

        except Exception as e:
            raise e

    def tra_Reply_ccUser(self, value):
        try:
            # uncomment below only when using TO user

            # self.driver.switch_to.default_content()
            # frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.mail_management_iframe_xpath)))
            # self.driver.switch_to.frame(frame1)

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_cc_list))).click()
            time.sleep(15)
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='wux-controls-abstract wux-controls-responsivetileview']//div[@class='wux-controls-responsivetileview-maincontent']//div[@class='wux-button-label-ellipsis-wrap wux-ui-is-rendered wux-controls-responsivetileview-description']//span[@class='searchItemSpan' and text()='" + value + "']"))).click()
            # logger_setup.logger.info("**** Template selected ")
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_person_ok_button))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    def tra_reply(self):

        # Method to click on reply button
        try:
            self.driver.switch_to.default_content()
            frameMail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.mail_management_iframe_xpath)))
            self.driver.switch_to.frame(frameMail)

            reply_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.reply_button_xpath)))

            reply_button.click()

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.tra_success_msg)))
            assert success_msg.is_displayed(), "Success message not displayed after replying TRA"
            # # # logger_setup.logger.info(" success msg located", success_msg)
            # time.sleep(3)
            #
            # self.dp.check_doc_properties(docTitle)

            time.sleep(10)
        except Exception as e:
            raise e

    def tra_reply_Message(self, value):

        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.mail_management_iframe_xpath)))
            self.driver.switch_to.frame(frame1)
            # logger_setup.logger.info("in frame 1")

            message_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.locate_mesg_field)))

            self.driver.execute_script("arguments[0].scrollIntoView(true);", message_field)

            frame2 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@class='cke_contents cke_reset']//iframe[@class='cke_wysiwyg_frame cke_reset']")))
            self.driver.switch_to.frame(frame2)

            # logger_setup.logger.info("in frame 2")
            message = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "//html[@dir='ltr']//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")))
            # logger_setup.logger.info("in Message field")
            # message.send_keys("Auto Replied")
            message.send_keys(value)
            time.sleep(10)
        except Exception as e:
            raise e

    # Verifying the TRANSMITAL & Replying to a transmittal - END ===========================================================

    # Verifying the TRANSMITAL & forwarding to a transmittal - START ===========================================================

    def click_forward_command(self):

        try:
            fwd_command_xpath = "//span[@class='fa fa-mail-forward close' and @title='Forward']"

            fwd_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, fwd_command_xpath)))
            fwd_button.click()

        except Exception as e:
            raise e

    def tra_fwd_toUser(self, username):
        try:

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_to_list))).click()
            time.sleep(15)
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='wux-controls-abstract wux-controls-responsivetileview']//div[@class='wux-controls-responsivetileview-maincontent']//div[@class='wux-button-label-ellipsis-wrap wux-ui-is-rendered wux-controls-responsivetileview-description']//span[@class='searchItemSpan' and text()='" + username + "']"))).click()
            # logger_setup.logger.info("**** forward Person selected ")
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_person_ok_button))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    def tra_forward(self):

        # Method to click on reply button
        try:
            self.driver.switch_to.default_content()
            frameMail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.mail_management_iframe_xpath)))
            self.driver.switch_to.frame(frameMail)

            fwd_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.forward_button_xpath)))

            fwd_button.click()

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.tra_success_msg)))
            assert success_msg.is_displayed(), "Success message not displayed after forwarding TRA"

            time.sleep(10)
        except Exception as e:
            raise e

    def selecting_Inbox_filters(self):
        try:
            self.driver.switch_to.default_content()
            frame_mail = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.mail_management_iframe_xpath)))
            self.driver.switch_to.frame(frame_mail)
            locate_filter = WebDriverWait(self.driver, 50).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_button)))
            locate_filter.click()
            time.sleep(1)

            out_filter = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_value_outstanding)))

            # # logger_setup.logger.info(" html info is %s", out_filter)

            # Check if the filter element is selected (active)
            out_filter_select = out_filter.get_attribute("attr-selected")
            if out_filter_select != 'true':
                print("Filter is not active for OUT")
                out_filter.click()
            else:
                print("Filter is active for OUT")
            time.sleep(1)

            na_filter = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.filter_value_NA)))
            # Check if the filter element is selected (active)
            na_filter_select = na_filter.get_attribute("attr-selected")
            if na_filter_select != 'true':
                print("Filter is not active for NA")
                na_filter.click()
            else:
                print("Filter is active for NA")
            time.sleep(1)

            inbox_filter = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.filter_value_Inbox)))

            # Check if the filter element is selected (active)
            inbox_filter_select = inbox_filter.get_attribute("attr-selected")
            if inbox_filter_select != 'true':
                print("Filter is not active for INBOX")
                inbox_filter.click()
            else:
                print("Filter is active for INBOX")
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.close_filter_window_event))).click()
            time.sleep(2)
        except Exception as e:
            raise e

    # Verifying the TRANSMITAL & forwarding to a transmittal - END ===========================================================


class iframes:  # all iframes locators

    iframeNMDocumentCntrl_xpath = "//div[@id='7zAw5w30gCwH0QgEjm01']//iframe[@id='frame-9sMywGd0g06qZr2-U046']"
    mail_management_iframe_xpath = "//div[@class='moduleWrapper']//iframe[@id='frame-9wOjNo70g06qNYY8Lm01']"
    tabDocumentUpload_xpath = "//a[contains(.,'Document Upload')]"
    tabTemporaryDocument_xpath = "//a[contains(.,'Temporary Document')]"
    tabRegisteredDocument_xpath = "//a[contains(.,'Registered Document')]"
    tabLegacyDocument_xpath = "//a[contains(.,'Legacy Document')]"
    select_files_xpath = "//div[@id='mass_upload']//div[contains(.,'Select File/s *')]//child::input[@id='input-19']"
    complete_upload = "//div[@role='progressbar']//i[contains(.,'100%')]"
    bt_inline_edit_du = "//button[@class='v-icon notranslate v-icon--link mdi mdi-pencil theme--light']"
    bt_mass_edit_du = "//div[@class='v-speed-dial v-speed-dial--bottom v-speed-dial--left v-speed-dial--direction-top']"
    bt_mass_edit_1 = "//button[@class='v-btn v-btn--is-elevated v-btn--fab v-btn--has-bg v-btn--round theme--dark v-size--small green']"
    mass_edit_form = "//div[@class='v-card__title']//span[contains(@class, 'headline') and text() = 'Mass Edit']"
    text_ms_title_field = "//label[text() = 'Title']/.."
    drp_ms_wo_field = "//label[text() = 'Work Order/Service Order']/.."
    drp_ms_status_field = "//label[text() = 'Status']/.."
    # ms_status_selection = "//div[contains(@class, 'v-list-item__title') and text() = 'For Review']"
    drp_ms_stage_field = "//label[text() = 'Stage']/.."
    # ms_stage_selection = "//div[contains(@class, 'v-list-item__title') and contains(text(), '03A')]"
    bt_update_all = "//span[contains(@class, 'v-btn__content') and text() = 'UPDATE ALL']"
    # select_a_document = "(//div[@class='v-input--selection-controls__ripple'])[3]"
    # select_a_document = "//a[contains(@href, '#') and text() = '02-ABI-BMN-3DM-000012']/../..//i[@class='v-icon notranslate mdi mdi-checkbox-blank-outline theme--light']"
    plus_menu_button = "//i[@class='v-icon notranslate mdi mdi-plus theme--dark']"
    # create_workflow_button = "//button[@class='v-btn v-btn--is-elevated v-btn--fab v-btn--has-bg v-btn--round theme--dark v-size--small yellow']//div[contains(@style, 'Create%20Workflow')]"
    widget_name = 'Document Register'
    reg_rows_per_page_filter = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='50']"
    # reg_rows_per_page_filter = "//div[@class='v-data-footer__icons-after']//button[@class='v-btn v-btn--icon v-btn--round v-btn--text theme--light v-size--default']"
    reg_rows_per_page_all = "//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='All']"
    all_rows_selected = "//div[@class='v-input__slot' and @aria-owns='list-119']//div[@class='v-select__slot']//div[@class='v-select__selection v-select__selection--comma' and text()='All']"

    create_workflow_button = "//div[@style='transition-delay: 0.2s;']//div[@class='v-responsive__content']"
    select_reasonForIssue = "//select[@name='IMP_WFReasonForIssue']/option[1]"
    wf_title = "//input[@name='IMP_WFTitle']"
    wf_create_button = "//button[@class='btn-primary btn hd-form-submit-hover hd-form-submit-focus']"
    wf_template_selector_button = "//div[@class='fa fa-search search']"
    template_page_locator = "//span[@class=' set-detail-view-title' and text()='Results']"
    template_select_from_list = "//div[@class='wux-controls-responsivetileview-maincontent']//span[@class='searchItemSpan search_item_in_apps' and text()='WK-Approve-Task-Template']"
    template_ok_button = "//div[@class='buttonContainer footer_button']//button[@id='id_in_app_ok' and text()='OK']"
    route_selection = "//div[@class='wux-tweakers wux-tweakers-urlobject']//a[@class='wux-tweakers-string-label' and text()='Not Started']"
    right_click_start_button = "//div[@class='wux-menu-cell wux-menu-push']//div[@data-wux-menu-item-uid='1']"
    iframe_Route_Management = "//div[@id='m_preview-7362fc']//iframe[@id='frame-preview-7362fc']"
    tra_person_ok_button = "//button[@id='id_in_app_ok']"
    tra_cc_list = "//div[@linked='IMP_CCList']"

    # constructor to initialise driver
    def __init__(self, driver):
        self.lp = LoginPage(driver)
        self.driver = driver
        self.dp = regDocument_properties(self.driver)

    # logger = LogGen.loggen()

    def navigate_to_tab_document_upload(self):

        # Method to navigate to the Document tab in Document Register widget

        try:
            # to get to the default iFrame
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tabDocumentUpload_xpath))).click()

        except Exception as e:
            raise e

    def navigate_to_tab_registered_document(self):

        #  Method to navigate to the Registered Document tab in Document Register widget

        try:
            self.driver.switch_to.default_content()
            frame1 = WebDriverWait(self.driver, 100).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 500).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.tabRegisteredDocument_xpath)))
            WebDriverWait(self.driver, 250).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tabRegisteredDocument_xpath))).click()
            time.sleep(15)

        except Exception as e:
            raise e

    def select_a_document(self, docTitle):
        # Method to select a document from reg doc tab and create WF
        try:
            doc_link_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']"
            checkbox_xpath = "//a[contains(@href, '#') and text() = '" + docTitle + "']/../..//div[@class='v-input--selection-controls__ripple']"

            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            #     (By.XPATH, self.all_rows_selected)))

            # Scroll the element into view
            doc_element = self.driver.find_element(By.XPATH, doc_link_xpath)
            ActionChains(self.driver).move_to_element(doc_element).perform()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath))).click()

        except Exception as e:
            raise e

    def create_workflow(self):
        try:

            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.plus_menu_button))).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.create_workflow_button))).click()
        except Exception as e:
            raise e

    def wf_creation_window(self, title):

        #  Method to input WF details in WF creation window
        try:
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.select_reasonForIssue))).click()
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.wf_title))).send_keys(title)
            try:
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.wf_template_selector_button))).click()
                time.sleep(15)
                # below "default_Content" code because to search for template, need to switch the frame
                # WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(
                #     (By.XPATH, self.template_page_locator)))

                self.driver.switch_to.default_content()
                WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.template_select_from_list))).click()

                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, self.template_ok_button))).click()
                time.sleep(5)

            except Exception as e:
                raise e

            self.driver.switch_to.default_content()
            time.sleep(5)
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
            self.driver.switch_to.frame(frame1)
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.wf_create_button))).click()
            time.sleep(5)

        except Exception as e:
            raise e

    def start_workflow(self):
        try:
            time.sleep(10)
            frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.iframe_Route_Management)))
            self.driver.switch_to.default_content(frame1)
            # logger_setup.logger.info"*** frame swicthed ***")
            route_element = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.route_selection))).click()
            ActionChains(self.driver).double_click(route_element).perform()

            # WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            #     (By.XPATH, self.right_click_start_button))).click()

        except Exception as e:
            raise e

    def tra_iframe_ccUser(self, user):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_cc_list))).click()
            time.sleep(15)
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='wux-controls-abstract wux-controls-responsivetileview']//div[@class='wux-controls-responsivetileview-maincontent']//div[@class='wux-button-label-ellipsis-wrap wux-ui-is-rendered wux-controls-responsivetileview-description']//span[@class='searchItemSpan' and text()='" + user + "']"))).click()
            # logger_setup.logger.info("**** Template selected ")
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, self.tra_person_ok_button))).click()
            time.sleep(5)
        except Exception as e:
            raise e

    # def select_file(self, filepath):
    #     '''
    #             Method to select files from local
    #             '''
    #     try:
    #         self.driver.switch_to.default_content()
    #         frame1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.iframeNMDocumentCntrl_xpath)))
    #         self.driver.switch_to.frame(frame1)
    #         WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.select_files_xpath))).send_keys(filepath)
    #         WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.complete_upload)))
    #
    #     except Exception as e:
    #         raise e
    #
    # # def update_document(self, title, wo, status, stage):
    # def update_document(self, title):
    #     '''
    #             Method to wait till completion of file upload
    #             '''
    #     try:
    #         WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.complete_upload)))
    #         WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.bt_mass_edit_du))).click()
    #         WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.bt_mass_edit_1))).click()
    #         WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #             (By.XPATH, self.mass_edit_form)))
    #         try:
    #             ''' Entering text into title field '''
    #             title_field = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                 (By.XPATH, self.text_ms_title_field)))
    #             title_field.click()
    #             time.sleep(2)
    #             title_field.send_keys(title)
    #
    #         except Exception as e:
    #             raise e
    #
    #         try:
    #             ''' selecting wo from dropdown '''
    #             ms_wo_selection = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                 (By.XPATH, self.drp_ms_wo_field)))
    #             ms_wo_selection.click()
    #             WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #                 (By.XPATH, self.ms_wo_list))).click()
    #
    #         except Exception as e:
    #             raise e
    #
    #         # # ms_wo_selection = Select(WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #         # #    (By.XPATH, self.drp_ms_wo_field))))
    #         # # ms_wo_selection.select_by_visible_text(wo)
    #         #
    #         # ms_status_selection = Select(WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #         #    (By.XPATH, self.drp_ms_status_field))))
    #         # ms_status_selection.select_by_visible_text(status)
    #         #
    #         # ms_stage_selection = Select(WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #         #    (By.XPATH, self.drp_ms_stage_field))))
    #         # ms_stage_selection.select_by_visible_text(stage)
    #         #
    #         # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
    #         #    (By.XPATH, self.bt_update_all))).click()
    #
    #     except Exception as e:
    #         raise e

    # -------- Transmittal Management START--------------------------------------------
