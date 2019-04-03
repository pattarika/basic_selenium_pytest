from sharepoint import SharePoint
import pytest
import unittest
#from unittest.mock import patch


class Test_Education(unittest.TestCase):
    
    @classmethod
    def setUp(request):
        sp = SharePoint('firefox', 'E:\\git\\pattarika\\basic_selenium_pytest\\account.txt')
        sp.login('pwongcha')

        yield
        sp.driver.close()

    @pytest.fixture()
    def test_create_newsite():
        sp = SharePoint()
        sp.goto_url('admin', '')
        title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
        sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', 'New SharePoint Site')
        sp.create_newsite(title, title + '_descr', title + '_url')

    def test_verify_navigation(self):
        title = '0_' + self.sp.getText('id', 'headerText1') + '_tmp'
        url = title + '_url'
        self.sp.goto_url('navigation', url)
        self.sp.wait(10, 'ctl00_PlaceHolderMain_ctl05_RptControls_bottomOKButton')

        # assert sp.is_checked('ctl00_PlaceHolderMain_globalNavSection_ctl03_inheritTopNavRadioButton') is True
        # assert sp.is_checked('ctl00_PlaceHolderMain_globalNavSection_ctl03_globalIncludeSubSites') is True
        # assert sp.is_checked('ctl00_PlaceHolderMain_currentNavSection_ctl03_inheritLeftNavRadioButton') is True
        # assert sp.is_checked('ctl00_PlaceHolderMain_currentNavSection_ctl03_currentIncludeSubSites') is True

    def test_verify_layout(self):
        title = '0_' + self.sp.getText('id', 'headerText1') + '_tmp'
        url = title + '_url'
        print(self.sp.goto_url('layout', url))

    def test_verify_history(self):
        title = '0_' + self.sp.getText('id', 'headerText1') + '_tmp'
        url = title + '_url'
        self.sp.goto_url('default', url)
        self.sp.wait(10, 'Ribbon.WikiPageTab-title')
        self.sp.click('id', 'Ribbon.WikiPageTab-title')
        self.sp.click_js('id', '\'' + 'Ribbon.WikiPageTab.EditAndCheckout.SaveEdit-SelectedItem' + '\'')
        self.sp.click('id', 'Ribbon.WikiPageTab-title')
        self.sp.click_js('id', '\'' + 'Ribbon.WikiPageTab.Manage.VersionDiff-Medium' + '\'')
        self.sp.click('id', 'ctl00_PlaceHolderMain_ctl00_ctl00_toolBarTbl_RptControls_diidIOVersions_LinkText')

    # @pytest.fixture
    # def test_delete_newsite(driver):
    #     sp = SharePoint(driver)
    #     sp.goto_url('admin')
    #     title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
    #     ID = sp.firstSiteCollectionID()
    #     sp.click('id', ID)
    #     sp.delete_newsite(ID, title)

    def test_siteup(self):
        with patch('SharePoint.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.sp.is_siteup()
            mocked_get.asset_called_with('https://education.sptest16.depaul.edu/')
            self.assertEqual(schedule, 'Success')

            mocked_get.return_value.ok = False

            schedule = self.sp.is_siteup()
            mocked_get.asset_called_with('https://educationXX.sptest16.depaul.edu/')
            self.assertEqual(schedule, 'Bad Response!')

if __name__ == '__main__':
    unittest.main()