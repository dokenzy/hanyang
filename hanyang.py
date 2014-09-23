# -*- coding: utf-8 -*-

# python: 3.4.1
# hanyang.py
# dokenzy@gmail.com
# license: MIT License

__version__ = '0.0.1'

from bs4 import BeautifulSoup
import requests
from datetime import datetime

# TODO:
# 주말에 오류 발생

cafes = ['학생복지관 학생식당',
         '학생회관 중식당',
         '교직원식당',
         '사랑방',
         '신교직원식당',
         '식학생식당',
         '제2생활관 식당',
         '행원파크']
days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일']

today = datetime.today().weekday()  # 요일의 인덱스. 월요일: 0
result = {}


def getSikdan(cafe_index):
    """
    선택한 식당의 이름, 위치, 운영 시간 등의 정보 및 식단을 가져온다.
    """
    url = 'http://www.hanyang.ac.kr/upmu/sikdan/sikdan_View.jsp?gb=1&code=%s' % (cafe_index + 1)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    general = soup.findAll('div', class_='tableStyle41Div')[0]
    cafe = {}
    cafe['식당명'] = general.findAll('img', alt='식당명')[0].parent.parent.td.text
    cafe['식당위치'] = general.findAll('img', alt='위치')[0].parent.parent.td.text
    cafe['운영시간'] = soup.findAll('div', class_='foodTime')[0].text
    result['식당정보'] = cafe
    tables = soup.select('#sikdang')[0].findAll('table')

    sikdans = []

    for table in tables:
        """
        1주일간의 식당 정보를 파싱해서 sikdans에 저장
        """
        sikdan = {}
        try:
            lunch = table.tbody.findAll('tr')[1].findAll('td')  # 중식
            lunch4000 = lunch[1].text.strip()
            lunch5000 = lunch[3].text.strip()
            dinner = table.tbody.findAll('tr')[2].findAll('td')  # 중식
            dinner1_menu = dinner[1].text.strip()
            dinner1_price = dinner[2].text.strip()
            dinner2_menu = dinner[3].text.strip()
            dinner2_price = dinner[4].text.strip()
            sikdan['lunch1'] = {'price': 4000, 'menu': lunch4000}
            sikdan['lunch2'] = {'price': 5000, 'menu': lunch5000}
            sikdan['dinner1'] = {'price': dinner1_price, 'menu': dinner1_menu}
            sikdan['dinner2'] = {'price': dinner2_price, 'menu': dinner2_menu}
            sikdans.append(sikdan)
        except:
            pass
    result['메뉴'] = sikdans


def getMenu(cafe_name='교직원식당'):
    """
    선택한 카페에 대한 식단을 가져온다.
    """
    # TODO:
    # 요일 선택할 수 있도록.
    # 현재는 오늘만 나옴
    cafe_index = cafes.index(cafe_name)
    getSikdan(cafe_index)
    today_menu = result['메뉴'][today]
    today_menu['date'] = datetime.today().strftime('%Y년 %m월 %d일')
    today_menu['day'] = days[today]
    return today_menu

print(getMenu()['dinner2']['menu'])
