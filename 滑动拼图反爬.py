from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import ImageChops
from PIL import Image
from io import BytesIO
import time

# 初始化对象
browser = webdriver.Chrome()
# 打开网页
browser.get('http://www.porters.vip/captcha/jigsawCanvas.html')
# 等待加载
time.sleep(5)

# 页面下拉到底部，保证截图完整
browser.execute_script("window.scrollTo(0,500)")
time.sleep(1)

# 定位滑块
jigsawCircle = browser.find_element(By.CSS_SELECTOR,'#jigsawCircle')
# 定位验证码图片
jigsawCanvas = browser.find_element(By.CSS_SELECTOR,'#jigsawCanvas')
# 截取初始图
before = jigsawCanvas.screenshot_as_png
# 点击并长按
action = ActionChains(browser)
action.click_and_hold(jigsawCircle).perform()

# 隐藏滑块
scripts = """
var missblock = document.getElementById('missblock');
missblock.style['visibility'] = 'hidden';
"""
browser.execute_script(scripts)

# 再次截图
after = jigsawCanvas.screenshot_as_png

# 调整图片模式，py 2.x版本的不用修改
image_a = Image.open(BytesIO(before)).convert("RGB")
image_b = Image.open(BytesIO(after)).convert("RGB")
# 使用ImageChops模块中的difference()方法对比图片像素的不同
diff = ImageChops.difference(image_b, image_a)
# 获取图片差异位置的坐标
diff_position = diff.getbbox()
# 结果 (211, 72, 250, 111)

# 移动并松开
action.move_by_offset(int(diff_position[0])-10,0)
action.release().perform()
time.sleep(3)

# 关闭浏览器
browser.close()
