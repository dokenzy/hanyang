# -*- coding: utf-8 -*-

# python: 3.4.1
# hanyang.py
# dokenzy@gmail.com
# license: MIT License

__version__ = '0.0.2'

from bs4 import BeautifulSoup
import requests
from datetime import datetime

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
isSat = False
result = {}

def getSikdan(tables):
    """
    월요일부터 토요일까지의 식단을 파싱해서 리턴
    """
    sikdans = []
    for table in tables:
        sikdan = {}
        try:
            # 점심 1
            lunch = table.tbody.findAll('tr')[1].findAll('td')  # 중식
            lunch1 = lunch[1].text.strip().split(',')
            lunch1_price = lunch[2].text.strip()
            sikdan['lunch1'] = {'menu': lunch1, 'price': lunch1_price}
            if not isSat:
                # 토요일은 lunch1 밖에 없음
                # lunch2
                lunch2 = lunch[3].text.strip()
                lunch2_price = lunch[4].text.strip()
                sikdan['lunch2'] = {'menu': lunch2, 'price': lunch2_price}
                # dinner1
                dinner = table.tbody.findAll('tr')[2].findAll('td')  # 중식
                dinner1_menu = dinner[1].text.strip()
                dinner1_price = dinner[2].text.strip()
                # dinner2
                dinner2_menu = dinner[3].text.strip()
                dinner2_price = dinner[4].text.strip()
                sikdan['dinner1'] = {'price': dinner1_price, 'menu': dinner1_menu}
                sikdan['dinner2'] = {'price': dinner2_price, 'menu': dinner2_menu}
        except:
            pass
        finally:
            sikdans.append(sikdan)
    return sikdans


def getInfo(cafe_index):
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

    result['메뉴'] = getSikdan(tables)


def getMenu(cafe_name='교직원식당', day=today):
    """
    선택한 카페에 대한 식단을 가져온다.
    """
    cafe_index = cafes.index(cafe_name)
    if day == 5:
        isSat = True
    getInfo(cafe_index)
    menu = result['메뉴'][day]
    menu['date'] = datetime.today().strftime('%Y년 %m월 %d일')
    menu['day'] = days[day]
    return menu

print(getMenu(day=4)['dinner1']['menu'])
