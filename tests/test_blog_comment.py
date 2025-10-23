from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
BLOG_TITLE_KEY = "Lorem ipsum dolor"

def _click_first(driver, wait, locators):
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click(); return
        except Exception:
            continue
    raise RuntimeError(f"Cannot click any of: {locators}")

def test_post_blog_comment():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(BASE_URL)
        _click_first(driver, wait, [
            (By.LINK_TEXT, "Blog"),
            (By.PARTIAL_LINK_TEXT, "Blog"),
            (By.CSS_SELECTOR, "a[title='Blog']"),
            (By.CSS_SELECTOR, "a[href*='blog']"),
        ])
        _click_first(driver, wait, [
            (By.LINK_TEXT, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"),
            (By.PARTIAL_LINK_TEXT, BLOG_TITLE_KEY),
            (By.CSS_SELECTOR, "a[href*='article_id']"),
        ])
        name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name*='name']")))
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        comment = driver.find_element(By.CSS_SELECTOR, "textarea")
        name.clear(); name.send_keys("blog tester")
        email.clear(); email.send_keys("tester@example.com")
        comment.clear(); comment.send_keys("My blog comment.")
        _click_first(driver, wait, [
            (By.XPATH, "//button[normalize-space()='Post comment']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'comment')]"),
        ])
        msg = wait.until(EC.presence_of_element_located((
            By.XPATH, "//*[contains(@class,'alert') or contains(@class,'success') or contains(@class,'message') or contains(@class,'notice')]"
        )))
        text = msg.text.lower()
        assert any(k in text for k in ["success","submitted","awaiting","pending","moderation"]), text
        assert ("blog" in driver.current_url) or ("article" in driver.current_url)
    finally:
        driver.quit()
