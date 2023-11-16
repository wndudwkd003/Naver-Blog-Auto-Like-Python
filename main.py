import os
import configparser
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

global DRIVER_URL, CHROME_URL, MAX_PAGE_COUNT
BLOG_URL = "https://section.blog.naver.com/"


def init_settings():
    global DRIVER_URL, CHROME_URL, MAX_PAGE_COUNT

    config = configparser.ConfigParser()
    config.read(os.getcwd() + os.sep + 'setting.ini', encoding='utf-8')

    DRIVER_URL = config.get('DEVICE', 'driver')
    CHROME_URL = config.get('DEVICE', 'chrome')
    MAX_PAGE_COUNT = int(config.get('PERSONAL', 'max_page_count'))

    print(DRIVER_URL)
    print(CHROME_URL)
    print(MAX_PAGE_COUNT)


def create_driver() -> webdriver.Chrome:
    # 크롬 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    # 불필요한 에러 메시지 없애기
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 크롬 드라이버 경로 설정
    service = Service(DRIVER_URL)

    # 크롬 경로 설정
    chrome_options.binary_location = CHROME_URL

    # 드라이버 객체 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    return driver


def main():
    init_settings()  # ini 파일 설정
    print()

    print('실행되는 크롬 브라우저에서 로그인 합니다.')
    print('로그인을 하고 크롬을 종료하지 않고 엔터를 입력합니다.')
    print('가능하면 크롬을 화면 제일 위로 두시길 바랍니다.')
    print('*주의 로그인 한 후 네이버 블로그 홈에서 벗어나면 안됩니다.')

    driver = create_driver()
    driver.get(BLOG_URL)

    input('> ')

    try:
        for i in range(1, MAX_PAGE_COUNT + 1):
            post_list = driver.find_elements(By.CSS_SELECTOR,
                                             "#content > section > div.list_post_article.list_post_article_comments > div")
            for post in post_list:

                title = post.find_element(By.CSS_SELECTOR, 'div > div.info_post > div.desc > a.desc_inner > strong').text
                print(f'제목: {title}')

                try:
                    like_btn = post.find_element(By.CSS_SELECTOR, 'div > div.info_post > div.comments > div > div > a')

                    if like_btn.get_attribute('aria-pressed') == 'false':
                        print(f'상태: 좋아요를 눌렀습니다.')
                        like_btn.click()
                        time.sleep(1)

                    else:
                        print('상태: 이미 눌러져 있습니다.')

                except:
                    print(f'상태: 좋아요를 누를 수 없습니다.')

                print()

            # 현재 페이지가 버튼의 마지막 페이지의 경우
            if i % 10 == 0:
                al = driver.find_elements(By.CSS_SELECTOR, '#content > section > div:nth-child(3) > div > a')
                al[-1].click()

            else:
                bottom_elements = driver.find_elements(By.CSS_SELECTOR,
                                                       '#content > section > div:nth-child(3) > div > span')
                for el in bottom_elements:
                    page_btn = el.find_element(By.CSS_SELECTOR, 'a')

                    # 다음 페이지로 넘어가기
                    if i + 1 == int(page_btn.text):
                        page_btn.click()
                        break

            time.sleep(1)



    except Exception as e:
        print(traceback.format_exc())
        print('더 읽을 페이지가 없습니다.')

    print('실행이 완료되어 프로그램을 종료합니다.')

    driver.close()


if __name__ == "__main__":
    main()
