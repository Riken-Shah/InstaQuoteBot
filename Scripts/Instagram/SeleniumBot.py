import os
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class SeleniumBot:
    def __init__(self, testing=False):
        self.username, self.password = self.__get_credentials()
        options = webdriver.ChromeOptions()
        if not testing:
            options.add_argument("--headless")
            options.add_experimental_option("detach", True)
        options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 2"})

        driver = webdriver.Chrome(executable_path=os.getenv('chrome_exec_path'),
                                  options=options)

        # Going to instagram
        self.main_url = "https://www.instagram.com/"
        driver.get(self.main_url)
        sleep(20)

        if testing:
            self.driver = driver
        self.__driver = driver

        # Logging In
        self.__login()
        self.close_all_popups()

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

    def __login(self):
        """
        Logging in to the account
        """
        login_button = self.__driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
        login_button.click()
        sleep(5)
        username_input = self.__driver.find_element_by_xpath("//input[@name='username']")
        username_input.send_keys(self.username)
        password_input = self.__driver.find_element_by_xpath("//input[@name='password']")
        password_input.send_keys(self.password)
        password_input.submit()
        sleep(10)

    def post(self, img_path, caption):
        """
        This function is used to post on instagram
        :param img_path: image path
        :param caption: caption
        :return: None
        """
        # Getting to home page
        self.__driver.get(self.main_url)
        sleep(5)
        # Closing all popups
        self.close_all_popups()
        # Uploading a file
        menu_item = self.__driver.find_element_by_xpath("//div[@role='menuitem']")
        menu_item.click()
        sleep(3)
        self.__upload_a_file('//*[@id="react-root"]/section/nav[2]/div/div/form/input', img_path)
        # Clicking on next button
        self.__driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
        sleep(3)
        # Writing caption
        self.__send_text_with_emoji(self.__driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']"),
                                    caption)
        # Clicking on share button
        self.__driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
        sleep(3)
        # Closing all popups
        self.close_all_popups()

    def story(self, img_path):
        """
        [WIP] Post a story on instagram
        *Not working
        :param img_path: Image path
        :return: None
        """
        self.close_all_popups()
        self.__driver.find_element_by_xpath("//svg[@aria-label='New Story']").click()
        sleep(3)
        self.__upload_a_file('//*[@id="react-root"]/section/nav[1]/div/div/form/input', img_path)
        self.__driver.find_element_by_xpath("//span[contains(text(),'Add to your story')]").click()
        sleep(3)

    def greet_new_users(self, username_list):
        """
        This function greets first time following user
        :param username_list: List of usernames
        :return: Boolean
        """
        # Closing all popups
        self.close_all_popups()
        for username in username_list:
            message = f"Hey @{username} 👋. Thanks a lot for following us.\n " \
                      f"I'll make sure to post daily powerful💪 quotes\n" \
                      f"Till then Be positive ✚ and\n" \
                      f"Keep Hustling 🏋️ ..."
            self.dm(username, message)
        return True

    def dm(self, username, message):
        """
        This function is used to send direct message to user
        :param username: Valid insta username
        :param message: Message
        :return: None
        """
        # Going to direct message
        self.__driver.get('https://www.instagram.com/direct/new/')
        sleep(5)
        # Searching for user
        self.__driver.find_element_by_xpath('//input[@name="queryBox"]').send_keys(username)
        sleep(5)
        # Clicking on user
        self.__driver.find_element_by_xpath(f'//div[contains(text(), "{username}")]').click()
        sleep(3)
        # Next
        self.__driver.find_element_by_xpath('//div[contains(text(), "Next")]').click()
        sleep(3)
        # Writing message
        self.__send_text_with_emoji(self.__driver.find_element_by_xpath('//textarea'), message)
        # Sending message
        self.__driver.find_element_by_xpath('//button[contains(text(), "Send")]').click()
        sleep(3)

    def close_all_popups(self):
        """
        Close all popups
        """
        # Closing reactivation message
        self.close_reactivated()
        # Closing notification
        self.close_notification()
        # Closing add to home popup
        self.close_add_to_home()

    def close_reactivated(self):
        """
        Close the reactivation message
        """
        try:
            not_now_btn = self.__driver.find_element_by_xpath("//a[contains(text(),'Not Now')]")
            not_now_btn.click()
            sleep(3)
        except NoSuchElementException:
            pass

    def close_notification(self):
        """
        Close the notification
        """
        try:
            close_notification_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
            close_notification_btn.click()
            sleep(3)
        except NoSuchElementException:
            pass

    def close_add_to_home(self):
        """
        Close the add to home pop up
        """
        try:
            close_add_home_btn = self.__driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
            close_add_home_btn.click()
            sleep(3)
        except NoSuchElementException:
            pass

    def __upload_a_file(self, input_xpath, file_path):
        """
        Upload a file to the browser
        :param input_xpath: xpath of the input element
        :param file_path: file path
        :return: None
        """
        # File Input Button
        self.__driver.find_element_by_xpath(input_xpath).send_keys(file_path)
        sleep(5)

    def __send_text_with_emoji(self, elem, text):
        """
        Send text to input element
        :param elem: Selenium element
        :param text: Text to send
        """
        # Activating Element
        elem.send_keys(' ')
        js_add_text_to_input = """
          const elm = arguments[0], txt = arguments[1];
          elm.value += txt;
          elm.dispatchEvent(new Event('change'));
          """
        self.__driver.execute_script(js_add_text_to_input, elem, text)
        elem.send_keys(' ')
        sleep(3)

    def comment(self, code, msg):
        """
        Comment on post
        :param code: Instagram Post Code
        :param msg: Comment text
        :return: Boolean
        """
        # Go to post comment section
        self.__driver.get(f'{self.main_url}p/{code}/comments')
        sleep(10)
        # Set text in comment
        self.__send_text_with_emoji(
            self.__driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']"),
            msg)
        # Post comment
        self.driver.find_element_by_xpath("//button[contains(text(),'Post')]").click()
        return True

    def exit(self):
        """
        Exits from the browser
        """
        self.__driver.quit()
        return True
