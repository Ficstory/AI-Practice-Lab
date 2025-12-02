# 📉 Stock Sentiment Analysis & Archiving System

## 📖 Project Overview
**토스증권 종목 토론방의 실시간 데이터를 수집하여 여론을 분석하는 데이터 파이프라인 프로젝트**입니다.
Selenium과 BeautifulSoup을 활용해 동적 웹 페이지의 댓글을 수집하고, OpenAI API를 통해 해당 종목에 대한 긍정/부정 여론을 분석하여 시각화된 정보를 제공하는 것을 목표로 했습니다.

---

## ⚙️ Tech Stack
- **Language**: Python 3.9
- **Framework**: Django 4.2
- **Crawling**: Selenium, BeautifulSoup4, Requests
- **Database**: SQLite
- **AI Analysis**: OpenAI API (GPT-3.5/4)

---

## 🎯 Key Features
1. **Dynamic Crawling (동적 수집)**
   - Selenium을 활용하여 JavaScript로 렌더링되는 실시간 댓글 데이터 수집
   - BeautifulSoup4를 이용한 HTML 파싱 및 데이터 정제
2. **Data Pipeline (데이터 저장 및 관리)**
   - 수집된 비정형 텍스트 데이터를 SQLite 데이터베이스에 구조화하여 저장
   - Django ORM을 활용한 데이터 조회 및 삭제(관리) 인터페이스 구현
3. **Sentiment Analysis (감성 분석)**
   - OpenAI API 프롬프트 엔지니어링을 통해 댓글의 긍정/부정/중립 여론 자동 분류
   - 단순 텍스트 수집을 넘어 데이터에 '인사이트'를 부여하는 과정 구현

---

## 🚀 Installation & Execution

### 1. Clone Project
```bash
git clone <your-repo-url>
cd Stock-Sentiment-Crawling
```

### 2. Set Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Django Server
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Run Crawler (Separate Script)
```bash
python crawlings/crawler.py
```

---

## 💡 Troubleshooting & Retrospective

### 🔹 Challenges & Solutions
- **동적 페이지 크롤링 이슈**: 초기에는 Requests 만으로 접근 시 데이터가 로드되지 않는 문제가 있었습니다. 이를 해결하기 위해 웹 브라우저를 직접 제어하는 Selenium을 도입하여 JavaScript 실행 후의 DOM을 가져오도록 개선했습니다.

- **데이터 가공**: 수집된 댓글에 불필요한 공백이나 특수문자가 포함되는 문제가 있어, 전처리 로직을 추가하여 데이터의 품질을 높였습니다.