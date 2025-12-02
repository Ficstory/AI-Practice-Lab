# crawlings/crawler.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager # webdriver-manager 임포트

def fetch_toss_comments(company_name, limit=20, max_scroll=10):
    # 크롬 드라이버 옵션
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 백그라운드에서 실행
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # webdriver-manager를 사용하여 자동으로 드라이버 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 결과를 담을 딕셔너리
    result = {
        'stock_code': None,
        'comments': []
    }

    try:
        # 1. Toss 메인 접속
        driver.get("https://www.tossinvest.com/")
        
        # 2. 회사명 검색
        # '/' 키를 보내 검색창을 활성화합니다.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys("/")
        
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )
        search_input.send_keys(company_name)
        search_input.send_keys(Keys.ENTER)

        # 3. 종목 코드 추출
        WebDriverWait(driver, 15).until(EC.url_contains("/stocks/"))
        current_url = driver.current_url

        parts = current_url.split("/")
        if "stocks" in parts:
            stock_code = parts[parts.index("stocks") + 1]
            result['stock_code'] = stock_code
        else:
            raise ValueError(f"종목코드를 추출할 수 없습니다: {current_url}")
        
        # 4. 커뮤니티 페이지 접속
        community_url = f"https://www.tossinvest.com/stocks/{stock_code}/community"
        driver.get(community_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main article"))
        )
        
        # 5. 댓글 수집
        comments_set = set() # 중복 저장을 막기 위해 set 사용
        last_height = driver.execute_script("return document.body.scrollHeight")

        for _ in range(max_scroll):
            spans = driver.find_elements(By.CSS_SELECTOR, "article span[class*='_60z0ev1']")
            
            for span in spans:
                text = span.text.strip()
                if text:
                    comments_set.add(text)
            
            if len(comments_set) >= limit:
                break
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5) # 페이지 로딩 대기

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        result['comments'] = list(comments_set)[:limit]

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return result