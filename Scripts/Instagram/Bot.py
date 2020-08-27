import os
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import subprocess


class Bot:
    def __init__(self, testing=False):
        self.img_path = ''
        self.caption = None
        options = webdriver.ChromeOptions()
        if not testing:
            options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 2"})

        driver = webdriver.Chrome(executable_path=os.getenv('chrome_exec_path'),
                                  options=options)
        url = "https://www.instagram.com"
        driver.get(url)
        sleep(3)
        if testing:
            self.driver = driver
        self.__driver = driver
        # Logging In
        try:
            self.__login()
        except NoSuchElementException:
            self.__driver.get(url)
            sleep(60)

        sleep(6)
        # Closing Some Pop-Ups
        self.close_reactivated()
        self.close_notification()
        self.close_add_to_home()
        sleep(4)

    @staticmethod
    def __get_credentials():
        """
        Returns a username and password from .env file
        """
        username = os.getenv('username')
        password = os.getenv('password')
        if not username or not password:
            raise ValueError('Username or Password value is not set in .env file')
        return username, password

    def post(self, img_path: str, caption: str):
        """
        Post a image on instagram
        """
        self.img_path = img_path
        self.caption = caption
        self.close_notification()
        self.close_add_to_home()
        sleep(2)
        self.__upload_a_file('//*[@id="react-root"]/section/nav[2]/div/div/form/input')
        sleep(6)
        self.close_notification()
        self.__final_process()
        sleep(3)
        self.close_notification()

    def story(self, img_path: str):
        """
        Post a story on instagram
        *Not working
        """
        self.img_path = img_path
        self.close_notification()
        sleep(2)
        self.close_add_to_home()
        sleep(2)
        self.__driver.find_element_by_css_selector("svg[aria-label='New Story']").click()
        sleep(2)
        self.__upload_a_file('//*[@id="react-root"]/section/nav[1]/div/div/form/input')
        sleep(4)
        self.__driver.find_element_by_xpath("//span[contains(text(),'Add to your story')]").click()
        sleep(5)

    def __login(self):
        """
        Log in to the account
        """
        username, password = self.__get_credentials()
        sleep(10)
        login_button = self.__driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
        login_button.click()
        sleep(3)
        username_input = self.__driver.find_element_by_xpath("//input[@name='username']")
        username_input.send_keys(username)
        password_input = self.__driver.find_element_by_xpath("//input[@name='password']")
        password_input.send_keys(password)
        password_input.submit()

    def close_reactivated(self):
        """
        Close the reactivation message
        """
        try:
            sleep(2)
            not_now_btn = self.__driver.find_element_by_xpath("//a[contains(text(),'Not Now')]")
            not_now_btn.click()
        except:
            pass

    def close_notification(self):
        """
        Close the notification
        """
        try:
            sleep(2)
            close_notification_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
            close_notification_btn.click()
            sleep(2)
        except:
            pass

    def close_add_to_home(self):
        """
        Close the add to home pop up
        """
        sleep(3)
        try:
            close_add_home_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
            close_add_home_btn.click()
            sleep(1)
        except:
            pass

    def __upload_a_file(self, input_path: str):
        """
        Upload a file to the browser
        :param input_path: xpath of the input element
        """
        # New Bot Button
        self.__driver.find_element_by_xpath("//div[@role='menuitem']").click()
        sleep(2)
        # File Input Button
        self.__driver.find_element_by_xpath(input_path)\
            .send_keys(self.img_path)
        sleep(2)

    def __final_process(self):
        """
        Final Step to Post on Instagram
        """
        # Next Button
        self.__driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
        sleep(1.5)
        caption_field = self.__driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
        caption_field.click()
        # Copy the Caption
        subprocess.run("pbcopy", universal_newlines=True, input=self.caption)
        sleep(3)
        # Past the caption
        caption_field.send_keys(Keys.SHIFT, Keys.INSERT)
        sleep(3)
        # Share Button
        self.__driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()

    def exit(self):
        """
        Exits from the browser
        """
        self.__driver.quit()
        return True
