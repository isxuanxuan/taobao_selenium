from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import re
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="q"]')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@class="btn-search tb-bg"]')))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="total"]')))
        get_products()
        return total.text
    except TimeoutError:
        return search()
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="input J_Input"]')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="btn J_Submit"]')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.XPATH,'//li[@class="item active"]/span'),str(page_number)))
        get_products()
    except TimeoutError:
        next_page(page_number)
def get_products():
    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@id="mainsrp-itemlist"]//div[@class="items"]/div')))
    page = browser.page_source
    sel = html.fromstring(page)
    items = sel.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"]/div')
    for item in items:
        product = {'店铺名称':item.xpath('.//div[@class="shop"]/a/span[2]/text()')[0],
                   '名称':item.xpath('.//div[@class="title"]/a/descendant-or-self::text()'),
                   '价格':'￥' + item.xpath('.//div[@class="price g_price g_price-highlight"]/strong/text()')[0],
                   '地区':item.xpath('.//div[@class="location"]/text()')[0]}

        print(product)
def main():
    total = search()
    total = int(re.search(r'(\d+)',total).group(1))
    for i in range(3,total + 1):
        next_page(i)
if __name__ == '__main__':
    main()

