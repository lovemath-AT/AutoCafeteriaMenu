import os
import datetime
import requests
from bs4 import BeautifulSoup


def save_menu_image(url, name):
    """
    주어진 URL에서 og:image 이미지를 가져와 dist 폴더에 저장합니다.
    """
    # 디렉터리 경로 설정
    folder_path = "dist"

    # 오늘 날짜 기반 폴더 생성
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    date_folder_path = os.path.join(folder_path, today_date)
    os.makedirs(date_folder_path, exist_ok=True)

    # 웹페이지 HTML 가져오기
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    # BeautifulSoup으로 og:image 찾기
    soup = BeautifulSoup(html, 'html.parser')
    og_image_tag = soup.find('meta', property="og:image")
    if not og_image_tag or not og_image_tag.get("content"):
        raise ValueError("og:image 태그를 찾을 수 없습니다.")
    image_url = og_image_tag["content"]

    # 이미지 다운로드
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # 파일 저장
    file_path = os.path.join(date_folder_path, f"{name}.jpg")
    with open(file_path, 'wb') as f:
        f.write(image_response.content)

    print(f"이미지가 {file_path}에 저장되었습니다.")


# URL 목록
urls = {
    "매일식당": "https://pf.kakao.com/_xchEJs/82405230",
    "푸드웰고시식당": "https://pf.kakao.com/_lxilAb/104034652",
    "38고시부페": "https://pf.kakao.com/_Vhnxob/107708565",
    "숙수의집": "https://pf.kakao.com/_essxkxj/107708521"
}

# 각 URL에 대해 이미지 다운로드
for name, url in urls.items():
    save_menu_image(url, name)
