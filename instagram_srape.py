from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests, os
from fake_useragent import UserAgent

class Instagram:
    def __init__(self,username = 'User login name',
                 password = 'user password', target_username = 'search username about'):
        self.fake_user = UserAgent()
        self.target_usernme = target_username
        self.username = username
        self.password = password
        self.main_url = 'https://www.instagram.com'
        self.driver = webdriver.Chrome()
        self.driver.get(self.main_url)
        sleep(3)
        self.login()
        self.search()
        sleep(2)
        self.scrolldown()
        sleep(2)
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.driver.close()
        if 'instagram' not in os.listdir():
            os.mkdir('instagram')
        self.path = os.path.join(os.getcwd(), 'instagram')
        self.download()

    def login(self):
        login_button = self.driver.find_element_by_xpath('//div[@class="gr27e"]//p[@class="izU2O"]/a')
        login_button.click()
        sleep(2)
        login_username = self.driver.find_element_by_xpath('//input[@name="username"]')
        login_username.send_keys(self.username)
        login_password = self.driver.find_element_by_xpath('//input[@name="password"]')
        login_password.send_keys(self.password)
        login_password.submit()
        sleep(2)
        notnow_button = self.driver.find_element_by_xpath('//button[@class ="aOOlW   HoLwm "]')
        notnow_button.click()


    def search(self):
        search_bar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
        search_bar.send_keys(self.target_usernme)
        sleep(2)
        search_value = self.driver.find_element_by_xpath('//a[@class ="yCE8d  "]')
        search_value.click()


    def scrolldown(self):
        self.posts = int(self.driver.find_element_by_xpath('//li[@class ="Y8-fY "]//span[@class ="-nal3 "]//span[@class ="g47SY "]').text)
        if self.posts>12:
            number_of_scroll = int(self.posts/12)
            for scroll in range(number_of_scroll):
                sleep(1)
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')


    def download(self):

        images = self.soup.find_all('img', class_='FFVAD')
        for index,image in enumerate(images,1):
            responce = requests.get(image['src'], headers = {'fake-user' : self.fake_user.chrome}).content
            content = 'image_' + str(index) + '.jpg'
            filename = os.path.join(self.path, content)
            with open(filename, 'wb') as img:
                img.write(responce)
                print('downloading ' + content + '...')



if __name__ == '__main__':
    scrape =  Instagram()
