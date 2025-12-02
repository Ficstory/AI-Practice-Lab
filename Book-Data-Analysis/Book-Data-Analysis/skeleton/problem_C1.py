import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]
load_dotenv() 


MY_TTBKEY = os.getenv('MY_TTBKEY')

ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    all_books = []
    url = ALADIN_SEARCH_URL
    for start in [1, 51]:
        params = {
           'TTBKey': MY_TTBKEY,    # API 키 정보
            'Query': topic,       # 검색할 키워드 정보
            'Output': 'js',         # 응답 형식 (JSON)
            'Version': '20131101',
            'MaxResults' : 50,
            'Start' : start      # API 버전
        }
        response = requests.get(url, params=params)    
        data = response.json()
        books = data.get('item', [])
        all_books.extend(books)
    return all_books[:max_results]

def save_books_to_json(data, filepath):
    path = Path(filepath)
    path.parent.mkdir(exist_ok=True)  # output 폴더 없으면 생성
    json_string = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(json_string, encoding='utf-8')
    print(f"✅ '{filepath}' 파일이 생성되었습니다.")

    

# 3. '인공지능' 도서 데이터를 처리하는 함수 정의
def process_ai_books():
    # 3.1 [ '인공지능' 관련 도서 검색 ]
    # fetch_books_by_topic()을 호출하여 '인공지능' 관련 도서를 100개 수집합니다.
    books = fetch_books_by_topic('인공지능', max_results=100) 

    # 3.2 [ 수집된 데이터에서 가격 정보가 있는 책 필터링 및 가격순 정렬 ]
    def get_price(book):
        return book['priceStandard']

    sorted_books = sorted(books, key=get_price, reverse=True) 
    unique_titles = set()
    top10 = []  
    for book in sorted_books:
        title = book['title']   
        if title not in unique_titles:
            unique_titles.add(title)
            top10.append(book)
        if len(top10) == 10:
            break

    # 3.3 [ 상위 10개 도서 선택 ]

    # 3.4 [ 상위 10개 도서 정보 출력 ]
    print('가격이 높은 순서대로 상위 10개 도서')
    count = 0
    for book in top10:
        count += 1 
        print(f"{count}. 제목: {book['title']}, 가격: {book['priceStandard']}원")
    json_data = [{'title': book['title'], 'author': book.get('author', '')} for book in top10]

    # 4.6 저장 함수 호출
    save_books_to_json(json_data, 'output/ai_top10_books.json')

    # 3.5 [ JSON 파일로 저장할 데이터 준비 ]
    # output/ai_top10_books.json 파일로 저장



# 함수 실행
if __name__ == '__main__':
    process_ai_books()
