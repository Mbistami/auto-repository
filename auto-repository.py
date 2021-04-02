from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
import sys, getopt
import pyperclip
import time

#TO REPLACE WITH YOUR OWN.
USERNAME="YOUR USERNAME";
PASSWORD="YOUR PATH";
WEBDRIVER_PATH = "chromedriver.exe PATH";
#END TO REPLACE.

REQUIREMENTS=['-pb', '-pv'];
MESSAGES={
    "usage" : "Usage : python auto-repostry.py <repostry-name> [OPTION] [OPTIONAL]\nOPTIONS :\n-pb = 'public repostry'\n-pv = 'private repostry'\nOPTIONAL:\n-r = 'initialize readme file\n-dhl = 'disable headless mode'",
    "finished" : "Link copied to clipboard!",
};

def checkArgs():
    if  (len(sys.argv) <= 2):
        return False;
    elif (REQUIREMENTS in sys.argv):
        return False;
    return True;

def login(driver):
    driver.get("https://github.com/login?return_to=%2Fjoin%3Fref_cta%3DSign%2Bup%26ref_loc%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home");
    element = driver.find_element(By.XPATH, '//input[@id="login_field"]');
    element.send_keys(USERNAME);
    element = driver.find_element(By.XPATH, '//input[@id="password"]');
    element.send_keys(PASSWORD);
    element = driver.find_element(By.XPATH, '//input[@value="Sign in"]');
    element.click();

def createRepostry(name, public, driver):
    visibility = 'repository_visibility_public';
    driver.get("https://github.com/new");
    element = driver.find_element(By.XPATH, '//input[@id="repository_name"]')
    element.send_keys(sys.argv[1])
    if (not public):
        visibility = 'repository_visibility_private';
    
    element = driver.find_element(By.XPATH, '//input[@id="{}"]'.format(visibility));
    element.click();
    if ('-r' in sys.argv):
        element = driver.find_element(By.XPATH, '//input[@id="repository_auto_init"]');
        element.click();

    time.sleep(2);
    driver.find_element(By.XPATH, '//form[@id="new_repository"]').submit();
    element = driver.find_element(By.XPATH, '//input[starts-with(@value, "git@github.com")]');
    pyperclip.copy(element.get_attribute("value"));

def main():
    public = True
    chrome_options = Options()
    if ('-dhl' not in sys.argv):
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH, chrome_options=chrome_options);
    if (not checkArgs()):
        print(MESSAGES["usage"]);
        return;
    if (not REQUIREMENTS[1] in sys.argv):
        public = not public;
    
    login(driver);
    createRepostry(sys.argv[1], public, driver);
    print(MESSAGES['finished']);
    
    
    

if __name__ == "__main__":
    main();