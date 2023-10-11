import pandas as pd
import numpy as np
import haversine as hs
import os, sys

os.chdir('C:\Users\User\Desktop\제발 되었으면 좋겠습니다\POI\POI')
# --------------------------------- 필독 ---------------------------
# df = pd.read_csv('link_seoul_ver3.csv', encoding='cp949') 에서의 
# link_seoul_ver.csv 파일 경로를 지정해주세요.
# ------------------------------------------------------------------ 
#
#
# ----------------- 입력 좌표 주어질때, 링크 추출 방법 --------------
# mapping_link에 위도 경도 쌍 ex) 37.547871, 126.997193 을 입력하면, 
# 좌표와 가장 가까운 링크 인덱스를 반환함
# 
# 추가 작업은 개개인 마다 다르기때문에 하지 않음. 
# -----------------------------------------------------------------
#
#
# -------------------------------- 함수 구성 --------------------------------------
# 1. mapping_link에 위경도 쌍을 넘겨주면, 
# link_haversine 함수 내에서 링크의 위경도 쌍과 입력한 좌표의 거리를 계산하여 
# 400m 이내인 링크만 추출 작업함.
#
# 2. 이후, link_shortest 함수를 통해 추출한 링크들과 좌표 간의 거리를 계산하여 
# 가장 짧은 값을 가지는 거리의 링크를 반환함.
# ---------------------------------------------------------------------------------


df = pd.read_csv('link_seoul_ver3.csv', encoding='cp949')
link = df['LINK_ID'].values
geometry = df['geometry']

geometry = geometry.str.replace('LINESTRING','')
geometry = geometry.str.replace('(','')
geometry = geometry.str.replace(')','')
geometry = geometry.str.replace(' ',',')
geometry = geometry.str.replace(',,',',')
geometry = geometry.str.split(',')
for i in range(len(geometry)):
    geometry[i].pop(0)

def distance(x1,y1,x2,y2,x3,y3):
    if x1 == x2:
        m = 0
    else:
        m = (y2-y1)/(x2-x1)
    a = m
    b = -1
    c = y1 - m*x1
    d = abs(a*x3 + b*y3 + c) / np.sqrt(a**2 + b**2)
    return d

def distance_link(link, geometry, x, y):
    d = []
    for i in range(0, len(geometry[link]) - 2, 2):
        x1 = float(geometry[link][i+1])
        y1 = float(geometry[link][i])
        x2 = float(geometry[link][i+3])
        y2 = float(geometry[link][i+2])
        d.append(distance(x1,y1,x2,y2,x,y))
    return min(d)

def distance_haversine(link, geometry, x, y):
    for i in range(len(geometry[link])):
        if i % 2 == 0:
            x1 = float(geometry[link][i+1])
            y1 = float(geometry[link][i])
            # 두 좌표간의 거리가 300m 이내라면 True로 반환
            # 300m 보다 적게하고싶다면 0.3을 수정하시면 됩니다.
            if hs.haversine((x,y),(x1,y1)) <= 0.2:
                return True
            else:
                continue
        else:
            continue
    

def link_haversine(geometry, x, y):
    link_haversine = []
    for i in range(len(geometry)):
        if distance_haversine(i,geometry,x,y) == True:
            link_haversine.append(i)
    return link_haversine

def link_shortest(link_haversine, geometry, x, y):
    d = []
    for i in range(len(link_haversine)):
        d.append(distance_link(link_haversine[i],geometry,x,y))
    return link_haversine[d.index(min(d))]


def mapping_link(x,y):
    linked_haversine = link_haversine(geometry, x, y)
    return link_shortest(linked_haversine, geometry, x, y)
    

loc1 = (37.547871, 126.997193)
print(mapping_link(loc1[0],loc1[1]))
# 입력은 위경도

culture1 = pd.read_csv("POI/문화/공연장.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture2 = pd.read_csv("POI/문화/관광궤도업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture3 = pd.read_csv("POI/문화/국제회의시설업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture4 = pd.read_csv("POI/문화/박물관,미술관.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture5 = pd.read_csv("POI/문화/전문휴양업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture6 = pd.read_csv("POI/문화/전통사찰.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture7 = pd.read_csv("POI/문화/종합유원시설업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture8 = pd.read_csv("POI/문화/종합휴양업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture9 = pd.read_csv("POI/문화/관광숙박업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture10 = pd.read_csv("POI/문화/관광펜션업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture11 = pd.read_csv("POI/문화/자동차야영장업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture12 = pd.read_csv("POI/문화/일반야영장업.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])
culture13 = pd.read_csv("POI/문화/영화상영관.csv", encoding='cp949', usecols=['좌표정보(x)', '좌표정보(y)'])

