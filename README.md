# 카뉴스집 (car_news.zip)
### 8개 자동차 관련 언론사에서 뉴스 스크래핑 및 분석

### 정보
- 접속 URL : <a href="http://carnewszip.com">http://carnewszip.com</a>
- 테이블 명세서 : <a href="https://docs.google.com/spreadsheets/d/1TOZSDXpLZaXQhyP-K11WmGR_dQ1tswQc181uI90sgF4/edit#gid=0">https://docs.google.com/spreadsheets/d/1TOZSDXpLZaXQhyP-K11WmGR_dQ1tswQc181uI90sgF4/edit#gid=0</a>
- 9개 자동차 언론사 : 오토헤럴드, 데일리카, 오토뷰, IT조선, 오토모닝, 오토다이어리, 카가이, 더드라이브

---

### 추가해야할 기능
- <del>회원(회원가입) >> 2020.12.08</del>
- <del>회원(로그인) >> 2020.12.07</del>
- <del>테마 (light모드, dark모드) >> 2020.12.01</del>
- <del>get_data.py 코드 리팩토링 >> 2020.12.01</del>
- 좋아요 기능 (좋아요 테이블 추가)
- 뉴스 클릭 수 카운팅 (표시)
- 메뉴 기능 추가 (각 카테고리별 언론사 보기, 언론사별 뉴스 모아보기)
- 카뉴스집 소개 구성 (간단하게)
- 뉴스 목록 페이징 처리 (스크롤 로드 방식)

---

### History

#### 2020.12.14 (월)
> 현재 각 언론사 목록 페이지에서 뉴스 제목, 요약내용만 가져오고 있는 상황(기사별 2~3줄)  
데이터 분석을 위한 각 상세페이지에 접근하여 기사 전체 내용 스크랩 필요

- 테이블 생성,수정,삭제
  - 테이블 명세서 히스토리 참조
- 뉴스 상세 데이터(제목, 내용) 스크랩

#### 2020.12.13 (일)
- 뉴스 클릭 수 카운팅 기능
  - UI 구성
  - models에 column추가 했으나 migrations되지 않는 문제로 기능 구현은 하지 못함
- 뉴스 목록 페이징 처리 (스크롤 로드 방식)
  - 효율적인 뉴스 목록 로드를 위한 구상 (param) 

#### 2020.12.12 (토)
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)
- GNB 메뉴 추가 (UI, 기능)
  - 모바일 최적화
  - param에 따른 데이터 및 화면 구성 
    - 메뉴 클릭 시 마다 통신을 해야하니 이게 최선의 방법인지는 고민 필요,,

#### 2020.12.11 (금)
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)
- GNB 메뉴 추가 (UI, 기능)
  - UI 구성
  - 뉴스 목록 urls, view 재정의 (카테고리, 언론사 별로 load를 위한 param 정의)

#### 2020.12.10 (목)
- 뉴스 TABLE 재설계(통합)
  - 뉴스 카테고리별로 테이블 구분 불필요 판단 > 통합뉴스 테이블에서 뉴스 카테고리 column을 생성
  - view(뉴스 수집 로직) 수정
- 뉴스 list 로드 방식 수정
  - ajax 호출 방식 (카테고리 클릭 시 해당 목록만 호출하여 노출)

#### 2020.12.09 (수)
- 로그인, 회원가입, 로그아웃 기능 구현
- SECRET_KEY, DB정보 분리 배포
 - 도메인 구입, 연결 (고대디 > <a href="http://www.carnewszip.com">http://www.carnewszip.com</a>)

#### 2020.12.08 (화)
- 로그인, 회원가입, 로그아웃 기능 구현
- Template 개선 (모바일 최적화)

#### 2020.12.07 (월)
- 로그인, 회원가입 Template 작업

#### 2020.12.04 (금)
- CentOS8 서버 셋팅
  - Python, Django
  - MariaDB

#### 2020.12.02 (수)
- 호스팅 서버 임대 (Conoha.jp)
- CentOS8 서버 셋팅
  - Python, Django
  - MariaDB

#### 2020.12.01 (화)
- 뉴스 가져오기 기능 웹 버튼으로 구현
- Skin기능 구현 (light, dark모드)

#### 2020.11.24 (화)
- 배포 (github, pythonanyway)

#### 2020.11.23 (월)
- 오토모닝 썸네일 비노출 이슈 확인 (URL변경되는 이슈?) > data 다시 수집 > 해결
- 뉴스 기사 좋아요 기능을 위한 column 추가 (LIKE_CNT)
- 배포 (github, pythonanyway)
  - settings.py파일은 ignore

#### 2020.11.19 (목)
- Django > 웹 구현 (뉴스 목록)
- list > today tag 추가 (오늘날짜 뉴스에 tag 표시)
- 시승기 카테고리 추가 (추가 언론사)
- 업계뉴스 카테고리 추가 (추가 언론사)

#### 2020.11.18 (수)
- Django > 웹 구현 (뉴스 목록)
- 시승기 카테고리 추가
- 업계뉴스 카테고리 추가
- 뉴데일리 중고차 이미지 URL 수정 
  - 이미지 스크랩 방어 코드로 되어 있어 분기처리로 대체 ('이미지를 불러올 수 없습니다')

#### 2020.11.17 (화)
- 불필요한 TABLE 정리
- Django > 웹 구현 (뉴스 목록)

#### 2020.11.11 (수)
- 뉴스 기사 형태소 분석
 - keyword 넣을 TABLE생성

#### 2020.11.10 (화)
- python에서 mariaDB연결
  - (ATC TEST DB)
- TABLE생성, 스크래핑한 뉴스 data INSERT

#### 2020.11.09 (월)
- 자동차 뉴스 사이트 4개 > 신차 뉴스, 중고차 뉴스 데이터 스크래핑
  - (오토헤럴드, 데일리카, 오토뷰, IT조선)
- python에서 mariaDB연결
  - (ATC TEST DB)