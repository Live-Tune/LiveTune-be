

---

# 📝 LiveTune 백엔드에 기여하기

기여에 관심 가져주셔서 감사합니다! LiveTune 플랫폼을 함께 개선해나가게 되어 기쁩니다. 본격적으로 시작하기 전에 이 가이드를 꼭 읽어주세요.  
[English CONTRIBUTING.md 바로가기](../CONTRIBUTING.md)

> [!IMPORTANT]  
> 본 프로젝트에 기여하고자 하는 개발자분들은 아래 내용을 꼭 숙지해 주세요.

## 📚 목차

- [⚙️ 사전 준비 사항](#️-사전-준비-사항)
- [🔧 프로젝트 설정](#-프로젝트-설정)
- [📝 기여 가이드라인](#-기여-가이드라인)
- [📁 폴더 구조](#-폴더-구조)

## ⚙️ 사전 준비 사항

기여하기 전에 아래가 준비되어 있어야 합니다:
- [Python](https://www.python.org/) (권장 버전: 3.9 이상) 및 pip
- [Flask](https://flask.palletsprojects.com/)와 [Flask-SocketIO](https://flask-socketio.readthedocs.io/) 에 대한 기본 이해

## 🔧 프로젝트 설정

개발 환경을 설정하기 전에 다음 내용을 참고해주세요.

레포지토리를 클론합니다.

```bash
git clone git@github.com:Live-Tune/LiveTune-be.git
cd LiveTune-be
```

가상 환경을 만들고 활성화합니다 (권장).

```bash
python -m venv venv
# Windows
# venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate
```

필요한 라이브러리 및 의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

루트 디렉토리에 [YouTube Data API 키](https://developers.google.com/youtube/v3/getting-started)를 포함한 `env.py` 파일을 생성합니다.

```python
YOUTUBE_API_KEY = "YOUR-API-KEY-HERE"
```

> [!important]  
> `env.py` 및 API 키는 **절대로 버전 관리에 포함되지 않아야 합니다.** 반드시 `.gitignore`에 포함되어 있는지 확인하세요.

서버를 실행하여 제대로 작동하는지 확인합니다.

```bash
python run.py
```

프론트엔드와 함께 테스트하고 싶다면, [#27 이슈](https://github.com/Live-Tune/LiveTune-be/issues/27)를 참고하여 프론트엔드 레포를 클론한 후 [설정 가이드](https://github.com/Live-Tune/LiveTune-fe/blob/main/CONTRIBUTING.md#-project-setup)를 따라 실행하면 됩니다.

이제 준비 완료입니다!

---

## 📝 기여 가이드라인

### 네이밍 규칙

#### 파일명

- Python (`.py`) 파일은 `snake_case`를 사용합니다. 예: `user_utils.py`, `room_models.py`

#### 함수, 변수, 메서드

- 함수, 변수, 메서드는 `snake_case`로 작성합니다. 예: `get_user_data`, `max_connections`    
- 클래스는 `PascalCase`로 작성합니다. 예: `UserSession`, `RoomManager`

### Git 사용 시

- 커밋할 때는 `git commit` 시 `-m` 옵션을 사용하지 않고 커밋 템플릿 형식(예: `.gitmessage`)을 따라 작성해주세요.    

### 개발 절차

1. 레포를 fork 합니다.
2. `main` 브랜치에서 `${YourGithubID}/기능명` 또는 `${YourGithubID}/이슈번호` 형식으로 브랜치를 만듭니다.  
    예: `john-doe/add-room-capacity-feature` 또는 `jane-doe/fix-123-login-bug`
3. 해당 브랜치에서 작업합니다.
4. 코드가 잘 포맷팅되어 있고 **주석이 충분히 달려 있는지** 확인합니다.
5. PR(Pull Request)을 요청할 때는 아래 항목을 포함해주세요:
    - 어떤 작업을 했는지 (간단한 요약)
    - 이 변경이 왜 필요한지 (관련 이슈 링크 또는 설명)
    - 어떻게 테스트할 수 있는지

---

## 📁 폴더 구조

백엔드 프로젝트 구조 개요:

```
LiveTune-be
├── app/                # 메인 애플리케이션 패키지
│   ├── __init__.py     # 애플리케이션 팩토리 및 블루프린트 등록
│   ├── routes.py       # API 엔드포인트 정의
│   ├── sockets.py      # WebSocket 이벤트 핸들러
│   └── utils.py        # 유틸리티 함수들
├── docker/
│   ├── Dockerfile
│   ├── dockerBuild.bat
│   ├── dockerImageLoad.bat
│   ├── dockerImageSave.bat
│   └── dockerRun.bat
├── .gitignore
├── env.py              # 환경변수 (버전 관리 제외 대상)
├── openapi.yaml        # API 문서
├── requirements.txt    # Python 패키지 의존성 목록
├── run.py              # 개발 서버 실행 스크립트
└── README.md           # 프로젝트 소개
```
