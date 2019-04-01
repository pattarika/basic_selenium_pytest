import pytest
from selenium import webdriver
from du_login import Login


def pytest_addoption(parser):
    parser.addoption("--driver", action = "store"
                               , default = "chrome"
                               , help = "Type in browser type")
    parser.addoption("--url"   , action = "store"
                               , default = "https://education.edu"
                               , help = "url")
    parser.addoption("--file", action = "store"
                                 , default = "account.txt"
                                 , help = "credentialFile")
    parser.addoption("--username", action = "store"
                                 , default = "username1"
                                 , help = "campus connect username")                                 


@pytest.fixture(scope="session", autouse=True)
def driver(request):
    driver = request.config.getoption("--driver")
    url = request.config.getoption("--url")
    credentialFile = request.config.getoption("--file")
    username = request.config.getoption("--username")

    sp = Login(credentialFile)    
    password = sp.get_pwd_by_username(username)

    if driver.lower() == 'chrome':
        driver = webdriver.Chrome()
    elif driver.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif driver.lower() == 'ie':
        driver = webdriver.Ie()
    else:
        raise Exception('Unknown webdriver type')    

    driver.delete_all_cookies()
    driver.get(url)    
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.find_element_by_link_text("Editor Login").click()
    driver.find_element_by_id("userNameInput").send_keys(username)
    driver.find_element_by_id("passwordInput").send_keys(password)
    driver.find_element_by_id("submitButton").click()
    driver.implicitly_wait(1)

    return driver

