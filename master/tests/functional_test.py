import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class HomePageTest(unittest.TestCase):

    websiteadres = 'http://193.191.187.253:8092/nl/'
    adminadres = 'http://193.191.187.253:8092/nl/admin/'

    admin = 'admin'
    adminmail = 'admin@example.com'
    adminwachtwoord = 'mocromaniac'

    gebruikermail = 'stijn.dirickx@hotmail.com'
    gebruikerwachtwoord = 'Abr9MPBfLN'


    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
         self.browser.get(self.websiteadres)
         self.assertIn('Viasofie', self.browser.title)

    def test_login_user_positive(self):
         self.browser.get(self.websiteadres)
         login = self.browser.find_element_by_id('login_link')
         login.click()
         self.browser.implicitly_wait(10)
         mail = self.browser.find_element_by_id('id_email')
         mail.send_keys(self.gebruikermail)
         password = self.browser.find_element_by_id('id_password')
         password.send_keys(self.gebruikerwachtwoord)
         login_form = self.browser.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey login-btn']")
         login_form.click()
         wait = WebDriverWait(self.browser, 5)
         wait.until(lambda browser: self.browser.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']"))
         accountbutton = self.browser.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']")
         self.assertIn('Account', accountbutton.text)


    def test_login_negative_wrongfields(self):
        driver = self.browser
        driver.get(self.websiteadres)
        login = driver.find_element_by_id('login_link')
        login.click()
        driver.implicitly_wait(10)
        mail = driver.find_element_by_id('id_email')
        mail.send_keys("novalidmail")
        password = driver.find_element_by_id('id_password')
        password.send_keys(self.gebruikerwachtwoord)
        login_form = driver.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey login-btn']")
        login_form.click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(lambda browser: self.browser.find_element_by_xpath("//p[@id='login-message']"))
        warning = driver.find_element_by_xpath("//p[@id='login-message']")
        self.assertIn("niet correct", warning.text)


    def test_login_negative_notexistingrecord(self):
        driver = self.browser
        driver.get(self.websiteadres)
        login = driver.find_element_by_id('login_link')
        login.click()
        driver.implicitly_wait(10)
        mail = driver.find_element_by_id('id_email')
        mail.send_keys("norecord@email.be")
        password = driver.find_element_by_id('id_password')
        password.send_keys('yCZjd4rbv7')
        login_form = driver.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey login-btn']")
        login_form.click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(lambda browser: self.browser.find_element_by_xpath("//p[@id='login-message']"))
        warning = driver.find_element_by_xpath("//p[@id='login-message']")
        self.assertIn("Email/Wachtwoord zijn niet correct!", warning.text)

    def test_login_admin(self):
         self.browser.get(self.websiteadres)
         login = self.browser.find_element_by_id('login_link')
         login.click()
         self.browser.implicitly_wait(10)
         mail = self.browser.find_element_by_id('id_email')
         mail.send_keys(self.adminmail)
         password = self.browser.find_element_by_id('id_password')
         password.send_keys(self.adminwachtwoord)
         login_form = self.browser.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey login-btn']")
         login_form.click()
         wait = WebDriverWait(self.browser, 5)
         wait.until(lambda browser: self.browser.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']"))
         accountbutton = self.browser.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']")
         accountbutton.click()
         admin_check = self.browser.find_element_by_xpath("//div[@class='btn-group account-dropdown open']/ul[@class='dropdown-menu']/li[1]/a")
         self.assertIn("Registreer verkoper", admin_check.text)


    def test_add_user(self):
        driver = self.browser
        driver.get(self.websiteadres)
        login = driver.find_element_by_id('login_link')
        login.click()
        driver.implicitly_wait(10)
        mail = driver.find_element_by_id('id_email')
        mail.send_keys(self.adminmail)
        password = driver.find_element_by_id('id_password')
        password.send_keys(self.adminwachtwoord)
        login_form = driver.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey login-btn']")
        login_form.click()
        wait = WebDriverWait(driver, 5)
        wait.until(lambda browser: driver.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']"))
        accountbutton = driver.find_element_by_xpath("//button[@class='btn btn-default dropdown-toggle']")
        accountbutton.click()
        add_user = driver.find_element_by_xpath("//div[@class='btn-group account-dropdown open']/ul[@class='dropdown-menu']/li[1]/a")
        add_user.click()

        driver.implicitly_wait(10)
        firstname = driver.find_element_by_id("id_first_name")
        firstname.send_keys("Stijn")
        lastname = driver.find_element_by_id("id_last_name")
        lastname.send_keys("den Tester")
        email = driver.find_element_by_id("id_email")
        email.send_keys("groep6mailer@gmail.com")
        user_form = driver.find_element_by_xpath("//button[@class='w3-btn w3-blue-grey']")
        user_form.click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(lambda browser: self.browser.find_element_by_xpath("//div[@class='panel panel-default w3-animate-opacity']/div[@class='panel-body']/p"))
        check = driver.find_element_by_xpath("//div[@class='panel panel-default w3-animate-opacity']/div[@class='panel-body']/p")
        self.assertIn("Account is succesvol aangemaakt", check.text)

        driver.get('http://193.191.187.253:8092/nl/admin/auth/user/')
        q = driver.find_element_by_xpath("/html/body[@class=' app-auth model-user change-list']/div[@id='container']/div[@id='content']/div[@id='content-main']/div[@id='changelist']/form[@id='changelist-form']/div[@class='results']/table[@id='result_list']/tbody/tr[@class='row2']/th[@class='field-username']/a")
        q.click()
        q = driver.find_element_by_xpath("/html/body[@class=' app-auth model-user change-form']/div[@id='container']/div[@id='content']/div[@id='content-main']/form[@id='user_form']/div/div[@class='submit-row']/p[@class='deletelink-box']/a[@class='deletelink']")
        q.click()
        q = driver.find_element_by_xpath("/html/body[@class=' app-auth model-user delete-confirmation']/div[@id='container']/div[@id='content']/form/div/input[2]")
        q.click()

    def test_add_estate(self):
        driver = self.browser
        driver.get('http://193.191.187.253:8092/nl/admin/master/pand/add/')
        q = driver.find_element_by_id('id_username')
        q.send_keys(self.admin)
        q = driver.find_element_by_id('id_password')
        q.send_keys(self.adminwachtwoord)
        q = driver.find_element_by_xpath("//form[@id='login-form']/div[@class='submit-row']/input")
        q.click()
        q = driver.find_element_by_id('id_referentienummer')
        q.send_keys('101144536')
        driver.find_element_by_xpath("//select[@name='user']/option[text()='Stijn_Dirickx']").click()
        q = driver.find_element_by_id('id_straat_naam')
        q.send_keys('Italielei')
        q = driver.find_element_by_id('id_huis_nummer')
        q.send_keys('02')
        q = driver.find_element_by_id('id_postcode')
        q.send_keys('2050')
        q = driver.find_element_by_id('id_stad')
        q.send_keys('Antwerpen')
        driver.find_element_by_xpath("//select[@name='status']/option[text()='Te Koop']").click()
        driver.find_element_by_xpath("//select[@name='staat']/option[text()='Bewoonbaar']").click()
        driver.find_element_by_xpath("//select[@name='type']/option[text()='Woning']").click()
        driver.find_element_by_xpath("//select[@name='fase']/option[text()='Verkoopsfase']").click()
        q = driver.find_element_by_id('id_prijs')
        q.send_keys('84000')
        q = driver.find_element_by_id('id_beschrijving')
        q.send_keys('Viva Italia, only pizza, pasta')
        q = driver.find_element_by_xpath("//form[@id='pand_form']/div/div[@class='submit-row']/input[@class='default']")
        q.click()


if __name__ == '__main__':
    unittest.main()
