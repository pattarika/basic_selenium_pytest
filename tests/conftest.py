import pytest
import allure
from selenium import webdriver
from app.sharepoint import SharePoint


def pytest_addoption(parser):
    parser.addoption('--browse', action = 'store'
                                , default = 'firefox'
            , help = 'Type in browser type (chrome, firefox, ie)')
    parser.addoption('--url'    , action = 'store'
                        , default = 'https://resources.sptest16.depaul.edu/'
                                , help = 'url')
    parser.addoption('--file'    , action = 'store'
                                 , default = './config/account.txt'
                                 , help = 'credentialFile')
    parser.addoption('--username', action = 'store'
                                 , default = 'pwongcha'
                                 , help = 'campus connect username')


@pytest.fixture(name='sp', scope='session')
def childsite(request):
    driver = request.config.getoption('--browse')
    url = request.config.getoption('--url')
    credentialFile = request.config.getoption('--file')
    username = request.config.getoption('--username')

    if driver.lower() == 'chrome':
        driver = webdriver.Chrome()
    elif driver.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif driver.lower() == 'ie':
        driver = webdriver.Ie()
    else:
        raise Exception('Unknown webdriver type')

    sp = SharePoint(driver, pytest='T')
    sp.login()

    yield sp
    driver.close()
