from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import base64
import numpy as np
import cv2
import random
# from page_source import MainForm
from main import MainForm

class Run():
    def __init__(self):
        # 账号和密码区块
        self.driver = webdriver.Chrome()
        self.driver.get("https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue%26utm_source%3Dbaidu-pinzhuan%26utm_medium%3Dcpc%26utm_campaign%3Dt_288551095_baidupinzhuan%26utm_term%3D0f3d30c8dba7459bb52f2eb5eba8ac7d_0_3ec3a567d542446dbcd153c13476aa06")
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, "div.login-tab.login-tab-r").click()
        self.driver.find_element(By.CSS_SELECTOR,"#loginname").send_keys("17689906102")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"#nloginpwd").send_keys("qw20130518")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "#loginsubmit").click()
        time.sleep(1)

        # 登陆区块
        self.slider()
        # 商品搜索，二次验证登陆
        self.search()

    def slider(self):
        """
        验证码登陆
        :return:
        """

        block = self.driver.find_element(
            By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img').get_attribute("src")
        img = self.driver.find_element(
            By.XPATH,
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
        block_ele = self.driver.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]')
        act = ActionChains(self.driver)
        act.click_and_hold(block_ele).perform()
        for i in self.offer(self.img_test(img, block)):
            act.move_by_offset(i, random.randrange(1, 3))
        act.release().perform()
        time.sleep(2)

        self.search()

    def search(self):
        """
        商品搜索操作，二次验证登陆
        :return:
        """

        # self.driver.find_element(By.CSS_SELECTOR,'#key').send_keys("净水器")
        # self.driver.find_element(By.CSS_SELECTOR,'.search-m .button').click()
        # time.sleep(2)
        # with open("京东.html","w",encoding="utf-8") as f:
        #     f.write(self.driver.page_source)

        try:
            # 搜索框定位
            self.driver.find_element(By.CSS_SELECTOR, '#key')
            return MainForm()
        except:
            Run()

    def offer(self,offset):
        """
        处理滑块轨迹
        :param offset:
        :return:
        """

        v, current = 0, 0
        mid = offset * 3 / 5
        tracks = []
        t = 0.6
        while current < offset:
            if current < round(mid):
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            current += s
            v = v + a * t
            tracks.append(round(s))
        return tracks
    
    def img_test(self,x,y):
        """
        缺口坐标处理区块
        :param x:
        :param y:
        :return:
        """

        x = base64.b64decode(x.split(",")[-1])
        img_array = np.frombuffer(x, np.uint8)
        img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        y = base64.b64decode(y.split(",")[-1])
        y = np.frombuffer(y, np.uint8)
        template = cv2.imdecode(y, cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
        value = cv2.minMaxLoc(res)[2][0]
        distance = value * 278 / 360
        return distance

def encrypt():
    """
    测试使用
    :return:
    """

    return MainForm()


if __name__ == "__main__":
    Run()