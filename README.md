hanyang
=======

버전: 0.0.2
한양대학교 식당 홈페이지를 파싱해서 식단정보만 가져오는 스크립트

## 사용방법
* getMenu(cafe_name='교직원식당', day=3): day는 0부터 월요일
* getMenu()['dinner2']) return {price: '4,000', menu: [반찬1, 반찬2, 반찬3, ...]}
* getMenu()['dinner2']['menu']) return [반찬1, 반찬2, 반찬3, ...]


## 식당이름(cafe_name)
* 학생복지관 학생식당
* 학생회관 중식당
* 교직원식당
* 사랑방
* 신교직원식당
* 식학생식당
* 제2생활관 식당
* 행원파크
