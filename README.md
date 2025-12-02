# 🤖 AI & Data Practice Lab

### 📌 Intro
데이터 수집(Crawling), 가공(Preprocessing), 그리고 AI 모델 활용(OpenAI API)을 실습한 코드 아카이브입니다.
단순한 구현을 넘어, 데이터를 목적에 맞게 분석하고 서비스에 적용하는 과정을 학습했습니다.

### 🛠 Tech Stack
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white"> <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white">

### 📂 Project List

#### 1. 📊 Stock Sentiment Crawling (주식 여론 분석 및 수집)
* **Description**: 금융 관련 웹사이트에서 종목 토론방 댓글 데이터를 크롤링하고, 긍정/부정 여론을 분석하는 프로젝트
* **Key Tech**:
    * `Selenium`, `BeautifulSoup`을 활용한 동적 웹 크롤링
    * `OpenAI API`를 활용한 텍스트 감성 분석 (Sentiment Analysis)
    * 수집된 데이터의 DB(SQLite) 적재 및 관리

#### 2. 📚 Book Data Analysis (도서 데이터 기반 추천 시스템)
* **Description**: 알라딘(Aladin) API와 LLM을 활용하여 도서 데이터를 수집하고, 사용자 맞춤형 추천 정보를 생성하는 프로젝트
* **Key Tech**:
    * `Rest API` 데이터 요청 및 JSON 파싱
    * `Pandas`를 활용한 데이터 필터링 및 통계 분석
    * `TTS (Text-to-Speech)` 라이브러리를 활용한 도서 요약 음성 변환

---
*This repository demonstrates the ability to handle data pipelines and AI integration.*
