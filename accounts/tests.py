from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path="/usr/local/Caskroom/chromedriver/86.0.4240.22/chromedriver")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('yuk.kgsm.ty02@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234@yuk')
        self.selenium.find_element_by_class_name('btn').click()

        # ページタイトルの検証
        self.assertEquals('お店一覧|likeshop', self.selenium.title)
