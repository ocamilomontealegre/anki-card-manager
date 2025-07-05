from time import sleep
from base64 import b64decode
from urllib.parse import quote
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_image(query: str) -> str:
    scaped_query = quote(query)
    url = f"https://www.google.com/search?tbm=isch&q={scaped_query}"
    options = ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )
    driver = Chrome(
        options=options, version_main=137, use_subprocess=True
    )

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#center_col"))
        )

        sleep(2)

        images = driver.find_elements(By.CSS_SELECTOR, "#center_col img[src^='data:image']")
        
        image_urls = []
        for idx, img in enumerate(images):
            try:
                src = img.get_attribute("src")
                image_urls.append(src)
                if len(image_urls) == 2:
                    break
            except Exception as e:
                print("ERROR: ", e)
        print("IMAGES: ", image_urls)
    except Exception as e:
        print("ERROR: ", e)
    finally:
        driver.quit()

    return ""


if __name__ == "__main__":
    get_image("two birds of a feather")
