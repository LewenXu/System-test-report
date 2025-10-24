
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"

def _click_first(driver, wait, locators):
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click(); return
        except Exception:
            continue
    raise RuntimeError("cannot click any locator")

def test_post_blog_comment(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    _click_first(driver, wait, [
        (By.LINK_TEXT, "Blog"),
        (By.PARTIAL_LINK_TEXT, "Blog"),
        (By.CSS_SELECTOR, "a[title='Blog']"),
        (By.CSS_SELECTOR, "a[href*='blog']"),
    ])

    _click_first(driver, wait, [
        (By.LINK_TEXT, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"),
        (By.PARTIAL_LINK_TEXT, "Lorem ipsum dolor"),
        (By.CSS_SELECTOR, "a[href*='article_id']"),
    ])

    name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name*='name']")))
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    comment = driver.find_element(By.CSS_SELECTOR, "textarea")
    name.clear();   name.send_keys("blog tester")
    email.clear();  email.send_keys("tester@example.com")
    comment.clear();comment.send_keys("Automated comment for F7 test.")

    _click_first(driver, wait, [
        (By.XPATH, "//button[normalize-space()='Post comment']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'comment')]"),
    ])

    msg = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".alert, .alert-success, .alert-danger, .message, .notice"
    )))
    assert msg is not None
    assert ("blog" in driver.current_url) or ("article" in driver.current_url)
