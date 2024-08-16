import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleAuthSpider(scrapy.Spider):
    name = 'google_auth_spider'
    start_urls = ['https://rocketreach.co/company?start=1&pageSize=10&keyword=va%20tech%20wabag']  # Replace with the URL you want to scrape

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_login)

    def parse_login(self, response):
        driver = response.meta['driver']
        wait = WebDriverWait(driver, 10)

        # Navigate to Google login page
        driver.get('https://accounts.google.com/signin')

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.ID, 'identifierId')))
        email_input.send_keys('salavatbatukhangame@gmail.com')  # Replace with your email
        driver.find_element(By.ID, 'identifierNext').click()

        # Enter password
        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password_input.send_keys('your-password')  # Replace with your password
        driver.find_element(By.ID, '3dZeV6GNn5zb6YHTAJ1U').click()

        # Wait for login to complete and redirect
        wait.until(EC.url_contains('https://rocketreach.co/company?start=1&pageSize=10&keyword=va%20tech%20wabag'))  # Replace with the URL you expect after login

        # Continue scraping after login
        yield SeleniumRequest(url=driver.current_url, callback=self.parse_data, dont_filter=True)

    def parse_data(self, response):
        # Implement your data extraction logic here
        item = {}
        item['title'] = response.css('a::text').get()
        print(item['title'])
        yield item