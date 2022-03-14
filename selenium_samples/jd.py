import sys
import time
import pyexcel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]

    option = Options()
    option.add_argument('--headless')
    # 创建一个没有界面的Chrome浏览器对象
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.jd.com')

    # 截图
    driver.save_screenshot('1.png')

    kw = driver.find_element(by=By.ID, value='key')
    kw.send_keys(keyword)
    kw.send_keys(Keys.RETURN)

    # 点击按销量排序
    # sort_btn = driver.find_element(by=By.XPATH, value='.//div[@class="f-sort"]/a[2]')
    # 当查找到我们需要的元素时，立即返回，否则最长等待10秒钟
    sort_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './/div[@class="f-sort"]/a[2]'))
    )
    sort_btn.click()
    driver.save_screenshot('2.png')

    has_next = True
    rows = []
    while has_next:
        time.sleep(3)
        cur_page = driver.find_element(by=By.XPATH, value='//div[@id="J_bottomPage"]//a[@class="curr"]').text
        print('------------------current page is %s-----------' % cur_page)
        # 先获取整改商品区域的尺寸坐标
        goods_list = driver.find_element(by=By.ID, value='J_goodsList')
        # 根据区域的大小绝定往下滑动多少
        y = goods_list.rect['y'] + goods_list.rect['height']
        # 执行JavaScript，滚动到页面底部
        driver.execute_script('window.scrollTo(0, %s)' % y)

        # 先获取所有的商品节点
        products = driver.find_elements(by=By.CLASS_NAME, value='gl-item')
        for p in products:
            row = {}
            sku = p.get_attribute('data-sku')
            row['price'] = p.find_element(by=By.CSS_SELECTOR, value='strong.J_%s' % sku).text
            row['name'] = p.find_element(by=By.CSS_SELECTOR, value='div.p-name>a>em').text
            row['comments'] = p.find_element(by=By.ID, value='J_comment_%s' % sku).text
            try:
                row['shop'] = p.find_element(by=By.CSS_SELECTOR, value='div.p-shop>span>a').text
            except Exception:
                row['shop'] = '无'
            print(row)
            rows.append(row)
        next_page = driver.find_element(by=By.CSS_SELECTOR, value='a.pn-next')
        if 'disabled' in next_page.get_attribute('class'):
            has_next = False
        else:
            next_page.click()
    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)
    driver.quit()




