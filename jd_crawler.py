import selenium
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素



kw = "手机"

driver = webdriver.Chrome(r"D:\browser\chromedriver.exe")
driver.get("https://jd.com")

# 隐式等待
driver.implicitly_wait(3)

# 获取输入框
kw_input = driver.find_element_by_id("key")

# 输入关键字
kw_input.send_keys(kw)

# 模拟点击回车
kw_input.send_keys(Keys.ENTER)

# 获取所有包含商品详细数据的li
items = driver.find_elements_by_class_name("gl-item")

# 需要获取的数据的：商品链接，价格，商品标题，评论数量
wait = WebDriverWait(driver, 10,0.5)

products = []
for i in range(2):
    for item in items:

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-img a')))
        url = item.find_element_by_css_selector(".p-img a").get_attribute("href")
        # print(url)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-price i')))
        price = item.find_element_by_css_selector(".p-price i").text
        # print(price)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-name a')))
        title = item.find_element_by_css_selector(".p-name a").text
        # print(title)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-commit strong a')))
        commit = item.find_element_by_css_selector(".p-commit strong a").text
        # print(commit)

        products.append({"url": url, "price": price, "title": title, "commit": commit})
# print(products)

# 如果要查询下一页的数据，则需要继续模拟浏览器发请求来点击下一页
    next_tag = driver.find_element_by_link_text(">")
    next_tag.click()

    time.sleep(3)
    items = driver.find_elements_by_class_name("gl-item")


print([i["commit"] for i in products])

for i in products:
    commit = i["commit"]
    commit = commit.strip("+")
    if "万" in commit:
        commit = commit.strip("万")
        commit = float(commit) * 10000
    else:
        commit = float(commit)
    i["commit"] = commit

res = sorted(products,key = lambda d:d["commit"])
print([i["commit"] for i in res])

print("最终销量冠军:",res[-1])