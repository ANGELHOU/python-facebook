from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Handler:
    def __init__(self):
        self.url = "https://www.facebook.com/ads/manager/creation/creation/?act=131173634067715&pid=p1"
        self.goal_xpath = '//*[@id="AdsCFObjectiveSelectorItem-BRAND_AWARENESS"]'
        self.audience_xpath = '//*[@id="u_0_0"]/div/div/div/div[1]/div[1]/div[2]/ul[3]/li[2]'
        self.market_input_element = '//*[@id="u_0_0"]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/div/div/div/div/div[7]/div/div/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div[3]/div[1]/span/label/input'
        self.data_div_selector = 'div[data-testid="targeting_detailed_targeting"]'
        self.username = "wswangsui@163.com"
        self.password = "462315ws"
        self.driver = webdriver.Chrome()

    def open_website(self):
        self.driver.get(self.url)
        email_element = self.driver.find_element_by_id("email")
        password_element = self.driver.find_element_by_id("pass")
        email_element.send_keys(self.username)
        password_element.send_keys(self.password)
        self.driver.find_element_by_name("login").click()

        #goal
        self.driver.find_element_by_xpath(self.goal_xpath).click()

        #audience
        self.driver.find_element_by_xpath(self.audience_xpath).click()

        #ajax
        time.sleep(20)
        input_element = self.driver.find_element_by_xpath(self.market_input_element)

        #click to show the select pannel
        input_element.send_keys('')
        input_element.click()

        #find the ul and li elements of the data
        lis = self.driver.find_element_by_css_selector(self.data_div_selector).find_element_by_css_selector("ul").find_elements_by_css_selector("li")

        for li in lis:
            self.preorder(li, 1)

        self.driver.quit()


    def preorder(self, li, level):
        print('-'*(level)+li.text+'\n')
        children = self.find_child(li)
        for child in children:
            self.preorder(child, level+1)


    def find_child(self, li):
        pre_result = self.get_pos(li)
        pre_num = len(pre_result[0]) - (pre_result[1] + 1)
        try:
            class_name = li.find_element_by_css_selector(" div >div>div").get_attribute("class")
            if class_name == '_6pe _6pg _4b91':
                li.click()
                post_result = self.get_pos(li)
                post_num = len(post_result[0]) - (post_result[1] + 1)
                diff = post_num - pre_num
                return post_result[0][post_result[1] + 1:post_result[1] + diff + 1]

        except:
            pass
        return []

    def get_pos(self, li):
        try:
            div_style = li.find_element_by_css_selector('div>div').get_attribute("style")
        except:
            div_style = li.find_element_by_css_selector('div').get_attribute("style")
        lis = self.driver.find_element_by_css_selector(self.data_div_selector).find_element_by_css_selector("ul").find_elements_by_css_selector("li")
        pos = -1
        for i in range(len(lis)):
            try:
                temp_div_style = lis[i].find_element_by_css_selector('div>div').get_attribute("style")
            except :
                temp_div_style = lis[i].find_element_by_css_selector('div').get_attribute("style")
            if(lis[i].text == li.text) and (temp_div_style == div_style):
                pos = i
                break
        return lis, pos

if __name__ == '__main__':
    test = Handler()
    test.open_website()