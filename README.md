# Minesweeper (지뢰찾기)

> **Note**: 이 프로젝트는 Google의 Gemini CLI의 도움을 받아 제작되었습니다.


Python의 `tkinter` 라이브러리를 사용하여 만든 클래식 지뢰찾기 게임입니다.

## 주요 기능

- **GUI 인터페이스**: `tkinter`를 사용하여 그래픽 사용자 인터페이스를 제공합니다.
- **난이도 조절**: 게임 시작 전, 다음 세 가지 난이도 중 하나를 선택할 수 있습니다.
  - **초급 (Easy)**: 9x9 크기, 지뢰 10개
  - **중급 (Medium)**: 16x16 크기, 지뢰 40개
  - **고급 (Hard)**: 16x30 크기, 지뢰 99개
- **사용자 정의 설정**: 원하는 판 크기(행, 열)와 지뢰 개수를 직접 설정하여 게임을 즐길 수 있습니다.
- **클래식 게임 플레이**:
  - **좌클릭**: 타일을 열어 지뢰가 있는지 확인합니다.
  - **우클릭**: 타일에 깃발(🚩)을 표시하거나 해제합니다.
  - **화음(Chord) 클릭**: 이미 열린 숫자 타일을 좌클릭하면, 주변에 해당 숫자만큼의 깃발이 꽂혀 있을 경우 나머지 타일들을 자동으로 열어줍니다.

## 요구 사항

- Python 3

`tkinter`는 Python 표준 라이브러리에 포함되어 있으므로 별도의 설치가 필요 없습니다.

## 실행 방법

1.  이 프로젝트 폴더로 이동합니다.
2.  터미널(cmd, PowerShell 등)에서 다음 명령어를 실행합니다.

    ```bash
    python minesweeper_gui.py
    ```

    또는 `py` 런처를 사용할 경우:

    ```bash
    py minesweeper_gui.py
    ```

3.  실행되면 설정 창이 나타납니다. 원하는 난이도를 선택하고 "Start Game" 버튼을 누르면 게임이 시작됩니다.

## 게임 방법

1.  **게임 목표**: 지뢰가 없는 모든 타일을 여는 것입니다.
2.  **타일 열기**: 아무 타일이나 마우스 좌클릭으로 엽니다.
3.  **숫자 의미**: 타일을 열었을 때 나타나는 숫자는, 그 타일 주변 8칸에 숨겨진 지뢰의 총개수를 의미합니다.
4.  **깃발 꽂기**: 숫자를 참고하여 지뢰가 있다고 확신하는 타일은 마우스 우클릭으로 깃발(🚩)을 꽂아 표시합니다.
5.  **게임 종료**:
    - **승리**: 지뢰가 없는 모든 타일을 열면 승리합니다.
    - **패배**: 지뢰가 있는 타일을 열면 게임에서 패배합니다.