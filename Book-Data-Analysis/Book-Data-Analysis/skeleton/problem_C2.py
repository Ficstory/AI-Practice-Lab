import os
import requests
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]
load_dotenv()
MY_TTBKEY = os.getenv('MY_TTBKEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# 3. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    """
    알라딘 API를 페이지네이션하여 최대 100개의 도서 데이터를 수집합니다.
    """
    all_books = []
    for start in [1, 51]:
        params = {
            'TTBKey': MY_TTBKEY,
            'Query': topic,
            'Output': 'js',
            'Version': '20131101',
            'MaxResults': 50,
            'Start': start
        }
        try:
            response = requests.get(ALADIN_SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            all_books.extend(data.get('item', []))
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")
            break
    return all_books[:max_results]


# 4. 책 데이터를 ChatGPT로 분류하는 함수 정의 (습관, 시간관리, 독서법, 기타)
def classify_books_with_gpt(books):
    # 4.1 [ 분류할 책 제목들을 전달하기 편한 문자열로 취합 ]
    titles = [book['title'] for book in books]
    # 각 제목을 번호와 함께 전달하여 AI가 개별적으로 인식하기 쉽게 합니다.
    titles_text = '\n'.join(f"{i+1}. {title}" for i, title in enumerate(titles))

    # 4.2 [ ChatGPT 대화 메시지 설정 (프롬프트 작성) ]
    # AI가 역할을 명확히 인지하고, JSON 형식으로만 응답하도록 지시합니다.
    prompt = f"""
    당신은 도서 분류 전문가입니다.
    아래의 책 제목 목록을 '습관', '시간관리', '독서법', '기타' 네 가지 카테고리 중 하나로 분류해주세요.
    반드시 아래의 JSON 형식과 동일하게 응답해야 하며, 다른 설명은 포함하지 마세요.

    [
      {{"title": "책 제목", "category": "분류 결과"}},
      {{"title": "책 제목", "category": "분류 결과"}}
    ]

    ---
    {titles_text}
    ---
    """

    # 4.3 [ 생성형 AI에 분류 요청 보내기 ]
    response = client.chat.completions.create(
        model='gpt-4o-mini', # JSON 모드를 지원하는 모델 사용
        messages=[
            {"role": "system", "content": "당신은 도서 목록을 JSON 형식으로 분류하는 유용한 조수입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1, # 일관된 출력을 위해 온도를 낮게 설정
        top_p=0.9,
        response_format={"type": "json_object"} # 응답 형식을 JSON으로 강제
    )
        
        # 4.4 [ ChatGPT의 응답을 가져와 JSON 으로 추출 ]
        # response_format을 사용하면 content가 바로 JSON 문자열이 됩니다.
    classification_result = json.loads(response.choices[0].message.content)
    return classification_result
    

# 5. [ 데이터를 JSON 파일로 저장하는 함수 정의 ]
def save_to_json(data, filename):
    output_dir = Path(filename).parent
    output_dir.mkdir(exist_ok=True) # 폴더가 없으면 생성
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 6. '독서' 도서 데이터를 처리하는 함수 정의
def process_reading_books():
    # 6.1 [ '독서'와 관련된 도서 검색 (100개) ]
    books = fetch_books_by_topic("독서", max_results=100)
    if not books:
        print("수집된 도서가 없어 프로그램을 종료합니다.")
        return

    # 6.2 [ 생성형 AI를 이용해 책 분류 ]
    classified_books = classify_books_with_gpt(books)
    if not classified_books:
        print("도서 분류에 실패했습니다.")
        return

    # 6.3 [ 분류된 책 정보를 JSON 파일로 저장 ]
    filename = "output/reading_habits.json"
    save_to_json(classified_books, filename)

    # 완료 메시지 출력
    print(f"'{filename}' 파일이 생성되었습니다.")


# 함수 실행
if __name__ == '__main__':
    process_reading_books()