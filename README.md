alfdaumdict : Daum Dictionary Workflow for Alfred
==============

Daum Dictionary Workflow for Alfred

Alfred에서 다음 사전을 검색하는 워크플로우입니다.

aesom 님의 [알프레드 워크플로우](https://github.com/aseom/alfred-workflows)를 python3 에 맞게 수정 및 개선하였습니다.

Install workflow
--------------
 
1. [requirements.txt](requirements.txt) 파일 내의 파이썬 패키지들을 설치한다.
2. `daumdict.alfredworkflow`를 다운로드 받아서 실행한다.

Usage
--------------
* `ddlan/ddeng {query}` {query} 자리에 원하는 단어를 입력하면 됩니다.

Build
--------------
```bash
bash ./make.sh
```

Requirements
--------------

* python3
  * [alfred-workflow-py3](https://github.com/kw-lee/alfred-workflow-py3.git)
  * requirements.txt

```bash
git submodule update --init --recursive
pip install -r requirements.txt
```

License
--------------
- MIT

Changelog
--------------

- `v0.0.1`: the first release