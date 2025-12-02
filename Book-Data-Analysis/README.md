# 📚 Intelligent Book Data Curation Service

## 📖 Project Overview
**알라딘(Aladin) Open API와 생성형 AI(GPT)를 결합한 도서 데이터 분석 및 추천 서비스**입니다.
외부 API를 통해 대량의 도서 데이터를 수집(ETL)하고, 사용자 맞춤형 분류를 수행하며, TTS(Text-to-Speech)를 활용해 도서 요약 음성 서비스를 제공하는 기능을 구현했습니다.

---

## ⚙️ Tech Stack
- **Language**: Python 3.9
- **Data Collection**: Requests (Aladin API)
- **AI & NLP**: OpenAI API, gTTS (Google Text-to-Speech)
- **Environment**: python-dotenv (Environment Variable Management)

---

## 🎯 Key Features
1. **Data Collection & Processing (데이터 수집 및 가공)**
   - '인공지능', '경제' 등 특정 키워드 기반 도서 데이터 100건 이상 자동 수집
   - 수집된 데이터의 평균 가격, 출판 연도 등 통계적 수치 분석 및 정렬
2. **AI-Driven Classification (AI 기반 자동 분류)**
   - OpenAI API를 활용하여 도서의 카테고리(습관, 시간관리, 독서법 등)를 문맥에 맞게 자동 분류
   - 단순 키워드 매칭이 아닌, 책 소개글(Description) 기반의 심층 분석 수행
3. **Audio Summary Generation (음성 요약 생성)**
   - 도서 제목과 핵심 요약 정보를 텍스트로 결합
   - gTTS 라이브러리를 활용하여 `.mp3` 포맷의 오디오 브리핑 파일 자동 생성
4. **Result Archiving**
   - 처리된 데이터를 용도에 맞게 JSON 및 TXT 형식으로 구조화하여 저장

---

## 💡 Key Learnings
* **API Integration**: 외부 Open API의 명세서를 분석하고, 인증 키(API Key)를 환경 변수(`.env`)로 안전하게 관리하는 법을 익혔습니다.
* **Prompt Engineering**: LLM(거대언어모델)에게 정확한 분류 작업을 시키기 위해 프롬프트를 최적화하는 과정을 경험했습니다.

* **Data Formatting**: JSON 응답 데이터를 파싱하여 원하는 필드만 추출하고 재가공하는 데이터 핸들링 역량을 키웠습니다.
