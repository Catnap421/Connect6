## Connect6

### 설치법(python 3.7.4 기준)

1. git clone
2. python -m venv venv // 가상환경 구성
3. (Window의 경우) >> ./venv/scripts/activate.ps1 
4. (venv 환경에서) pip install -r requirements.txt 
5. python main.py

### 빌드하기 (exe 파일 만들기)

1. (venv 실행) >> ./venv/scripts/activate.ps1
2. pip install cx_freeze
3. python setup.py build
4. build 디렉토리를 따라가면 exe파일 존재

### 주의사항

소스코드는 윈도우에서만 동작한다.

빌드한 파일의 파일의 경우, 경로 상에 한글이 존재하지 않아야 실행이 가능하다.

### Notion

https://www.notion.so/bleum/96846fe4c90341cdbebc500ef690cf96