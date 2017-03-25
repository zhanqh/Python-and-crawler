from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
)

browser = webdriver.PhantomJS(desired_capabilities=dcap)
browser.set_window_size(1400,900)

agent = browser.execute_script("return navigator.userAgent")
print(agent)
browser.get('http://httpbin.org/get')
print(browser.page_source)
browser.close()
