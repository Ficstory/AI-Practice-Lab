import os
import requests
from pathlib import Path
from gtts import gTTS
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


# 3. [ 도서 정보를 텍스트 파일로 저장하는 함수 정의 ]
# 책 정보를 "제목, 저자, 소개" 형식으로 변환하여 txt 파일로 저장
def save_books_info(books, filename):
    output_dir = Path(filename).parent
    output_dir.mkdir(exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        for book in books:
            title = book.get('title', '제목 없음')
            author = book.get('author', '저자 정보 없음')
            description = book.get('description', '소개 정보가 없습니다.')
            
            f.write(f"제목: {title}\n")
            f.write(f"저자: {author}\n")
            f.write(f"소개: {description}\n")
            f.write("-" * 20 + "\n") # 각 도서 정보 구분선

    print(f" {filename} 파일이 생성되었습니다.")
    return filename


# 5. [ 텍스트 파일을 오디오 파일로 변환하는 함수 정의 ]
def create_audio_file(text_file, audio_file):
    with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
    if not text_content.strip():
        print("텍스트 파일에 내용이 없어 오디오 파일을 생성하지 않습니다.")
        return

    tts = gTTS(text=text_content, lang='ko')
    tts.save(audio_file)
    print(f"{audio_file} 파일이 생성되었습니다.")


# 6. [ 음악 관련 도서 데이터를 처리하는 함수 정의 ]
def process_music_books():
    output_dir = Path('output')
    txt_filename = output_dir / 'music_books_info.txt'
    mp3_filename = output_dir / 'music_books.mp3'
    
    # 6.1 [ '음악' 주제의 도서 데이터 수집 ]
    music_books = fetch_books_by_topic('음악', max_results=10)
    if not music_books:
        print("음악 관련 도서를 찾지 못했습니다.")
        return

    # 6.2 [ 도서 정보를 텍스트 파일로 저장 ]
    save_books_info(music_books, txt_filename)

    # 6.3 [ 텍스트 파일을 오디오 파일로 변환 ]
    create_audio_file(txt_filename, mp3_filename)

    print("모든 작업이 완료되었습니다.")


# 함수 실행
if __name__ == '__main__':
    process_music_books()
