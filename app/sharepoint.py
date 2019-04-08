import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.du_login import Login


class SharePoint():

    def __init__(self, driver=None, pytest='T'):
        with open('./config/config.yaml') as f:
            config = yaml.safe_load(f)

        self.site = config['url_config']['site']
        self.admin_pg = config['url_config']['admin']
        self.setting_pg = config['url_config']['site_manager']
        self.nav_pg = config['url_config']['navigation']
        self.logo_pg = config['url_config']['logo']
        self.default_pg = config['url_config']['default']
        self.layout_pg = config['url_config']['layout']
        self.username = config['credential']['username']
        self.browser = config['browser']['type']
        self.driver = driver
        self.credential = Login(config['file']['credential'])        

        if pytest == 'F':
            if self.browser.lower() == 'chrome':
                self.driver = webdriver.Chrome()
            elif self.browser.lower() == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser.lower() == 'ie':
                self.driver = webdriver.Ie()
            else:
                raise Exception('Unknown webdriver type')
            self.driver.delete_all_cookies()

        self.driver.get(self.site)

    def login(self):
        password = self.credential.get_pwd_by_username(self.username)

        assert self.driver.find_element_by_link_text('Editor Login').text == 'Editor Login'
        url = self.driver.find_element_by_link_text('Editor Login').get_attribute('href')        
        self.driver.get(url)
        
        self.wait(5, 'userNameInput')
        self.driver.find_element_by_id('userNameInput').send_keys(self.username)
        self.driver.find_element_by_id('passwordInput').send_keys(password)
        self.driver.find_element_by_id('submitButton').click()
        self.driver.implicitly_wait(1)

    def click_js(self, type, text):
        if type == 'id':
            self.driver.execute_script('document.getElementById(' + text + ').click()')
        if type == 'class':
            self.driver.execute_script('document.getElementsByClassName(' + text + ').click()')

    def click(self, type, text):
        if type == 'id':
            self.driver.find_element_by_id(text).click()
        if type == 'text':
            self.driver.find_element_by_text(text).click()
        if type == 'link_text':
            self.driver.find_element_by_link_text(text).click()
        if type == 'xpath':
            self.driver.find_element_by_xpath(text).click()
        if type == 'css':
            self.driver.find_element_by_css_selector(text).click()

    def create_newsite(self, title, descr, url):
        value = 'ctl00_PlaceHolderMain_idTitleDescSection_ctl01_TxtCreateSubwebTitle'
        self.wait(15, value)

        self.find_by_id('ctl00_PlaceHolderMain_idTitleDescSection_ctl01_TxtCreateSubwebTitle', 'send_keys', title)
        self.find_by_id('ctl00_PlaceHolderMain_idTitleDescSection_ctl02_TxtCreateSubwebDescription', 'send_keys', descr)
        self.find_by_id('ctl00_PlaceHolderMain_idUrlSection_ctl01_TxtCreateSubwebName', 'send_keys', url)
        self.click('id', 'ctl00_PlaceHolderMain_ctl00_RptControls_BtnCreateSubweb')

        if self.is_error() is True:
            self.go_back()
            return False
        else:
            self.goto_url('admin')
            return True

    def delete_newsite(self, title):
        self.hoover_and_click('id', 'SmtToolbarDropdownAction4_t')
        self.click('link_text', 'Delete')

        if EC.alert_is_present:
            alert = self.driver.switch_to.alert
            alert.accept()

        time.sleep(2)
        # self.driver.refresh()
        self.goto_url('admin')
        assert title not in self.driver.page_source

    def find_by_id(self, id_value, action, fld_value):
        if action == 'clear':
            return self.driver.find_element_by_id(id_value).clear()
        if action == 'send_keys':
            return self.driver.find_element_by_id(id_value).send_keys(fld_value)
        if action == 'get_attribute':
            return self.driver.find_element_by_id(id_value).get_attribute(fld_value)

    def firstSiteCollectionID(self):
        frame = self.find_by_id('OLDiv', 'get_attribute', 'innerHTML')
        soup = BeautifulSoup(frame, 'html.parser')
        table = soup.find(lambda tag: tag.name == 'table'
                                and tag.has_attr('id')
                                and tag['id'] == 'ObjectList1_Grid1')
        columns = table.find('tr', {'class': 'ms-vb2'})
        self.driver.siteID = columns.find('input')['id']
        assert self.driver.siteID is not None
        return self.driver.siteID

    def get_sitename(self):
        self.goto_url('admin')

        frame = self.find_by_id('OLDiv', 'get_attribute', 'innerHTML')
        soup = BeautifulSoup(frame, 'html.parser')
        table = soup.find(lambda tag: tag.name == 'table'
                                    and tag.has_attr('id')
                                    and tag['id'] == 'ObjectList1_Grid1')
        rows = table.find('tr', {'class': 'ms-vb2'})
        self.siteName = rows.find('td', {'class': 'ms-vb'}).text
        return self.siteName.strip()

    def get_browser_title(self):
        return self.driver.find_element_by_tag_name('h1').text

    def goto_url(self, name, url=None):
        if name == 'admin':
            self.driver.get(self.site + self.admin_pg)
        if name == 'setting':
            self.driver.get(self.site + url + self.setting_pg)
        if name == 'navigation':
            self.driver.get(self.site + url + self.nav_pg)
        if name == 'logo':
            self.driver.get(self.site + url + self.logo_pg)
        if name == 'default':
            self.driver.get(self.site + url + self.default_pg)
        if name == 'layout':
            self.driver.get(self.site + url + self.layout_pg)
            html = self.driver.page_source
            return html
    
    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')    
    
    def getText(self, typ, text_value):
        if typ == 'id':
            txt = self.driver.find_element_by_id(text_value)
        assert txt.text is not None
        return txt.text

    def hoover(self, typ, value):
        if typ == 'id':
            elm = self.driver.find_element_by_id(value)
        if typ == 'text':
            elm = self.driver.find_element_by_text(value)
        if typ == 'link_text':
            elm = self.driver.find_element_by_link_text(value)

        ActionChains(self.driver).move_to_element(elm).perform()

    def hoover_and_click(self, typ, value):
        if typ == 'id':
            elm = self.driver.find_element_by_id(value)
        if typ == 'text':
            elm = self.driver.find_element_by_text(value)
        if typ == 'link_text':
            elm = self.driver.find_element_by_link_text(value)

        ActionChains(self.driver).move_to_element(elm).click().perform()

    def is_checked(self, ID):
        return self.driver.find_element_by_id(ID).is_selected()

    def is_error(self):
        return 'something went wrong' in self.driver.page_source

    def link_action(self):
        frame = self.find_by_id('OLDiv', 'get_attribute', 'innerHTML')
        soup = BeautifulSoup(frame, 'html.parser')
        table = soup.find(lambda tag: tag.name == 'table'
                                and tag.has_attr('id')
                                and tag['id'] == 'ObjectList1_Grid1')
        rows = table.find('tr', {'class': 'ms-vb2'})
        id = rows.find('td', {'class': 'ms-vb'}).find('a')['id']
        return id

    def wait(self, time, elementID):
        try:
            wait = WebDriverWait(self.driver, time)
            wait.until(EC.visibility_of_element_located((By.ID, elementID)))
        except:
            pass

    def toolbar_action(self, id_name, txt_name, label):
        self.hoover_and_click('id', id_name)
        self.click('link_text', txt_name)
        # assert label in self.driver.page_source