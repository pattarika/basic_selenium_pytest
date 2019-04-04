import pytest

# @pytest.fixture(name="sp", scope='module', autouse=True)
# def setup():
#     url = 'https://education.sptest16.depaul.edu'
#     username = 'pwongcha'
#     file = 'account.txt'
#     browser = 'firefox'
#     sp = SharePoint(browser, file, username)
#     sp.login()
#     sp.goto_url('admin','')

#     yield sp
#     sp.driver.close

@pytest.mark.skip
def test_create_newsite(sp):
    title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
    sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', 'New SharePoint Site')
    sp.create_newsite(title, title + '_descr', title + '_url')


def test_verify_navigation(sp):
    title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
    url = title + '_url'
    sp.goto_url('navigation', url)
    sp.wait(10, 'c`tl00_PlaceHolderMain_ctl05_RptControls_bottomOKButton')


def test_verify_layout(sp):
    title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
    url = title + '_url'
    sp.goto_url('layout', url)


def test_verify_history(sp):
    title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
    url = title + '_url'
    sp.goto_url('default', url)
    sp.wait(10, 'Ribbon.WikiPageTab-title')
    sp.click('id', 'Ribbon.WikiPageTab-title')
    sp.click_js('id', '\'' + 'Ribbon.WikiPageTab.EditAndCheckout.SaveEdit-SelectedItem' + '\'')
    sp.click('id', 'Ribbon.WikiPageTab-title')
    sp.click_js('id', '\'' + 'Ribbon.WikiPageTab.Manage.VersionDiff-Medium' + '\'')
    sp.click('id', 'ctl00_PlaceHolderMain_ctl00_ctl00_toolBarTbl_RptControls_diidIOVersions_LinkText')


# @pytest.fixture
# def test_delete_newsite(driver):
#     sp = SharePoint(driver)
#     sp.goto_url('admin')
#     title = '0_' + sp.getText('id', 'headerText1') + '_tmp'
#     ID = sp.firstSiteCollectionID()
#     sp.click('id', ID)
#     sp.delete_newsite(ID, title)

# def test_siteup(sp):
#     with patch('SharePoint.requests.get') as mocked_get:
#         mocked_get.return_value.ok = True
#         mocked_get.return_value.text = 'Success'

#         schedule = self.sp.is_siteup()
#         mocked_get.asset_called_with('https://education.sptest16.depaul.edu/')
#         self.assertEqual(schedule, 'Success')

#         mocked_get.return_value.ok = False

#         schedule = self.sp.is_siteup()
#         mocked_get.asset_called_with('https://educationXX.sptest16.depaul.edu/')
#         self.assertEqual(schedule, 'Bad Response!')
