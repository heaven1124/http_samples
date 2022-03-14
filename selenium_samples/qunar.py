import sys
import time
import pyexcel
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]

    option = Options()
    # 创建一个没有界面的Chrome浏览器对象,
    # Chrome-headless 是无界面版的Chrome
    # option.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get('https://flight.qunar.com/')

    # driver.refresh()
    # driver.forward()
    # driver.back()
    # driver.current_url
    # 执行JavaScript，滚动到页面底部
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    # 执行异步JavaScript代码
    # driver.execute_async_script('send_xml_request()')
    # 获取整个页面的源码
    # driver.page_source
    # 隐式等待
    # driver.implicitly_wait(10)
    # 查找一个按钮，最长等待10秒
    # --显示等待
    dest = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@name="toCity"]'))
    )
    # dest = driver.find_element(by=By.XPATH, value='//input[@name="toCity"]')
    dest.send_keys('成都')
    time.sleep(1)
    dest.send_keys(Keys.RETURN)
    driver.find_element(by=By.CSS_SELECTOR, value='button.btn_search').click()

    flights = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="m-airfly-lst"]/div[@class="b-airfly"]'))
    )

    for f in flights:
        fdata = {}
        airlines = f.find_elements(by=By.XPATH, value='.//div[@class="d-air"]')
        fdata['airlines'] = [airline.text.replace('\n', '-') for airline in airlines]
        fdata['depart'] = f.find_element(by=By.XPATH, value='.//div[@class="sep-lf"]').text
        fdata['duration'] = f.find_element(by=By.XPATH, value='.//div[@class="sep-ct"]').text
        fdata['dest'] = f.find_element(by=By.XPATH, value='.//div[@class="sep-rt"]').text
        fake_price = list(f.find_element(by=By.XPATH, value='.//span[@class="prc_wp"]/em/b[1]').text)
        covers = f.find_elements(by=By.XPATH, value='.//span[@class="prc_wp"]/em/b[position()>1]')
        for c in covers:
            index = int(c.value_of_css_property('left')[:-2]) // c.size['width']
            fake_price[index] = c.text
        fdata['price'] = ''.join(fake_price)
        print(fdata)

    driver.quit()



