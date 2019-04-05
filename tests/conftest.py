import pytest
from selenium import webdriver
# from app.du_login import Login
from app.sharepoint import SharePoint


def pytest_addoption(parser):
    parser.addoption('--browser', action = 'store'
                                , default = 'firefox'
            , help = 'Type in browser type (chrome, firefox, ie)')
    parser.addoption('--url'    , action = 'store'
                        , default = 'https://resources.sptest16.depaul.edu/test/'
                                , help = 'url')
    parser.addoption('--file'    , action = 'store'
                                 , default = './config/account.txt'
                                 , help = 'credentialFile')
    parser.addoption('--username', action = 'store'
                                 , default = 'pwongcha'
                                 , help = 'campus connect username')


@pytest.fixture(name='sp', scope='session')
def childsite(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    credentialFile = request.config.getoption('--file')
    username = request.config.getoption('--username')

    if browser.lower() is None:
        driver = webdriver.Firefox()
    elif browser.lower() == 'chrome':
        driver = webdriver.Chrome()
    elif browser.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif browser.lower() == 'ie':
        driver = webdriver.Ie()
    else:
        raise Exception('Unknown webdriver type')

    sp = SharePoint(driver, pytest='T')
    sp.login()
    sp.goto_url('admin', '')

    yield sp
    driver.close()
