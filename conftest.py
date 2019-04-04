import pytest
from selenium import webdriver
# from app.du_login import Login
from app.sharepoint import SharePoint


def pytest_addoption(parser):
    parser.addoption("--browser", action = "store"
                               , default = "firefox"
                               , help = "Type in browser type (chrome, firefox, ie)")
    parser.addoption("--url"   , action = "store"
                               , default = "https://education.sptest16.depaul.edu"
                               , help = "url")
    parser.addoption("--file", action = "store"
                                 , default = "E:\\git\\pattarika\\basic_selenium_pytest\\account.txt"
                                 , help = "credentialFile")
    parser.addoption("--username", action = "store"
                                 , default = "pwongcha"
                                 , help = "campus connect username")


@pytest.fixture(name="sp", scope="session", autouse=True)
def authenticate(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    credentialFile = request.config.getoption("--file")
    username = request.config.getoption("--username")

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

    driver.delete_all_cookies()

    sp = SharePoint(driver, credentialFile, username)
    sp.driver.get(url)
    sp.login()
    sp.goto_url('admin','')
    
    yield sp
    driver.close()

# @pytest.fixture(scope="session")
# def get_file(request):
#     return str(request.config.getoption("--file"))

# @pytest.fixture(scope="session")
# def get_username(request):
#     return str(request.config.getoption("--username"))
