# Minesweeper (브라우저 버전)

간단한 브라우저용 지뢰찾기 게임입니다. 이 저장소에는 세 가지 버전(브라우저 JS, tkinter GUI 스켈레톤, 콘솔 버전) 중 브라우저 실행 가능한 `minesweeper.js`가 포함되어 있습니다.

특징
- 첫 클릭 안전(첫 칸과 인접 칸에 지뢰 배치 제외)
- 좌클릭: 칸 열기(0인 경우 주변 자동 개방)
- 우클릭: 깃발 토글
- 승리 / 패배 감지
- 난이도 조정(행/열/지뢰 수)

파일 구성
- index.html — 게임 UI(브라우저에서 열기)
- minesweeper.js — 게임 로직(브라우저용, DOM 기반)
- minesweeper_gui.py — tkinter 기반 GUI 스켈레톤(미구현 메서드들)
- minesweeper5.3.py — 콘솔(텍스트) 버전 일부(미완성)

세 파일(비교)
----------------
다음은 저장소에 있는 세 가지 구현 파일의 주요 차이점과 현재 상태입니다.

- `minesweeper.js` (브라우저용)
   - 실행 환경: 웹 브라우저(HTML + CSS + JavaScript)
   - 상태: 동작 완료(브라우저에서 즉시 플레이 가능)
   - 입력 방식: 좌클릭(열기), 우클릭(깃발)
   - 핵심 기능: 첫 클릭 안전 처리(첫 칸 주변에 지뢰 미배치), 인접 지뢰 수 계산, 0일 때 주변 자동 개방(플러드 필), 깃발 토글, 승리/패배 판정
   - 배포: GitHub Pages로 곧바로 배포 가능

- `minesweeper_gui.py` (tkinter GUI 스켈레톤)
   - 실행 환경: 데스크톱 Python (tkinter 필요)
   - 상태: 구조(클래스, 이벤트 핸들러 등)와 UI 골격은 존재하나 여러 메서드가 미구현 상태
   - 의도된 동작: 윈도우 기반 인터페이스, 마우스 이벤트 처리, 설정 다이얼로그 등 GUI 중심 기능
   - 참고: `minesweeper.js`의 로직(지뢰 배치, reveal/flag/승패 판단)을 포팅하면 빠르게 완성할 수 있음

- `minesweeper5.3.py` (콘솔/텍스트 버전)
   - 실행 환경: 터미널(콘솔 출력)
   - 상태: 부분 구현 또는 골격 상태(완전 동작하지 않을 수 있음)
   - 특징 및 문제점: 출력에 전각 문자(예: 전각 숫자/기호)를 사용하면 터미널에서 문자 폭이 2칸으로 취급되어 열 정렬이 어긋남. 출력 정렬을 안정화하려면 반각 문자 사용 또는 `wcwidth` 같은 폭 계산 라이브러리를 이용해 패딩을 조정해야 함

비교 포인트 요약
- 실행 가능성: `minesweeper.js`(완성) > `minesweeper_gui.py`(미완성) ≈ `minesweeper5.3.py`(미완성)
- 입력 모델: 이벤트 기반(GUI/브라우저) vs 입력-루프(콘솔)
- 첫 클릭 안전 처리: `minesweeper.js`는 구현, 파이썬 파일들은 미구현이거나 확인 필요
- 권장 조치: 콘솔 정렬 문제는 전각 문자 교체 또는 `wcwidth` 적용, tkinter GUI는 JS 로직을 참고해 메서드 구현 권장


로컬에서 실행하기
1. 간단히 파일을 브라우저에서 열기:
   - 파일 매니저에서 `index.html` 더블클릭 또는
   - 브라우저에서 `file:///path/to/index.html`로 열기
2. 간단한 로컬 서버(권장):
   ```bash
   cd /home/pyeongju/ws2/minesweeper
   python3 -m http.server 8000
   # http://localhost:8000/ 접속
   ```

GitHub Pages에 배포
- `index.html`과 `minesweeper.js`를 리포지토리 루트에 커밋한 뒤,
  1. 새 브랜치(예: gh-pages)를 만들고 푸시:
     ```bash
     git switch -c gh-pages
     git add index.html minesweeper.js README.md
     git commit -m "Add browser Minesweeper and docs"
     git push -u origin gh-pages
     ```
  2. GitHub 리포지토리 설정(Settings) → Pages에서 `gh-pages` 브랜치와 루트(/)를 소스로 선택.
  3. 잠시 후 https://<your-username>.github.io/<repo>/ 에서 플레이 가능.

주의
- Flatpak으로 설치된 VS Code 등 환경에서는 시스템 라이브러리 접근 문제가 있을 수 있으니 로컬 브라우저에서 직접 확인하세요.
- `minesweeper_gui.py`와 `minesweeper5.3.py`는 현재 미완성 상태입니다. 필요한 경우 JS 로직을 참고해 완성 가능합니다.

라이선스 및 기여
- 간단한 개인/학습용 프로젝트입니다. 원하시면 라이선스 파일 추가해 드립니다.
- 기여: 이슈/풀리퀘스트 환영합니다.