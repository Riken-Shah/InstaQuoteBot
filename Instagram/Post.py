import os
from time import sleep
from selenium import webdriver
from env__ import username, password, chrome_exec_path
from selenium.webdriver.common.keys import Keys
import subprocess


class Post:
    def __init__(self, testing=False):
        self.img_path = ''
        self.caption = None
        options = webdriver.ChromeOptions()
        if not testing:
            options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 2"})

        driver = webdriver.Chrome(executable_path=chrome_exec_path,
                                  options=options)
        driver.get("https://www.instagram.com")
        sleep(3)
        self.__driver = driver
        # Logging In
        self.__login()
        sleep(6)
        # Closing Some Pop-Ups
        self.close_reactivated()
        self.close_notification()
        self.close_add_to_home()
        sleep(4)

    def post(self, img_path: str, caption: str):
        self.img_path = img_path
        self.caption = caption
        self.close_notification()
        self.close_add_to_home()
        sleep(2)
        self.__upload_a_file()
        sleep(6)
        self.close_notification()
        self.__final_process()
        sleep(3)
        self.close_notification()
        self.img_path = os.path.abspath(os.getcwd()) + '/'
        self.caption = None

    def __login(self):
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
        try:
            sleep(2)
            not_now_btn = self.__driver.find_element_by_xpath("//a[contains(text(),'Not Now')]")
            not_now_btn.click()
        except:
            pass

    def close_notification(self):
        try:
            sleep(2)
            close_notification_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
            close_notification_btn.click()
            sleep(2)
        except:
            pass

    def close_add_to_home(self):
        sleep(3)
        try:
            close_add_home_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
            close_add_home_btn.click()
            sleep(1)
        except:
            pass

    def __upload_a_file(self):
        # New Post Button
        self.__driver.find_element_by_xpath("//div[@role='menuitem']").click()
        sleep(2)
        # File Input Button
        self.__driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/form/input')\
            .send_keys(self.img_path)
        sleep(2)

    def __final_process(self):
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
        self.__driver.quit()
        return True


