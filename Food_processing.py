import sys, os
import numpy as np
import pandas as pd
import pyproj
import folium

os.chdir('C:/Users/User/Desktop/Please_give_me_a_chance/POI/POI')

food1 = pd.read_csv("POI_Ori/식품/fulldata_07_21_02_P_집단급식소.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food2 = pd.read_csv("POI_Ori/식품/fulldata_07_22_18_P_제과점영업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food3 = pd.read_csv("POI_Ori/식품/fulldata_07_23_01_P_단란주점영업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food4 = pd.read_csv("POI_Ori/식품/fulldata_07_23_02_P_유흥주점영업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food5 = pd.read_csv("POI_Ori/식품/fulldata_07_24_01_P_관광식당.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food6 = pd.read_csv("POI_Ori/식품/fulldata_07_24_04_P_일반음식점.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
food7 = pd.read_csv("POI_Ori/식품/fulldata_07_24_05_P_휴게음식점.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])

food_num = ['food1', 'food2', 'food3', 'food4', 'food5', 'food6', 'food7', 'food8', 'food9', 'food10', 'food11', 'food12', 'food13']
food_name = ['집단급식소', '제과점영업', '단란주점영업', '유흥주점영업', '관광식당', '일반음식점', '휴게음식점']

def project_array(coord, p1_type, p2_type):
    """
    좌표계 변환 함수
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) epsg:5179
    - p2_type: 출력 좌표계 정보 ex) epsg:4326
    """
    p1 = pyproj.Proj(init=p1_type)
    p2 = pyproj.Proj(init=p2_type)
    fx, fy = pyproj.transform(p1, p2, coord[:, 3], coord[:, 4])
    
    return np.dstack([fx, fy])[0]

def data_processing(name):
    name.drop(name[(name['영업상태명'] == '폐업')].index, inplace=True)
    name = name[name['영업상태명'].notna()]
    name = name[~name['영업상태명'].str.contains('정지')]
    name = name[name['소재지전체주소'].str.contains('서울특별시') & name['소재지전체주소'].notna()]
    
    name['좌표정보(x)'] = pd.to_numeric(name['좌표정보(x)'], errors="coerce")
    name['좌표정보(y)'] = pd.to_numeric(name['좌표정보(y)'], errors="coerce")
    name = name.dropna(axis=0)
    name.index = range(len(name))
    coord = np.array(name)

    p1_type = "epsg:2097"
    p2_type = "epsg:4326"

    result = project_array(coord, p1_type, p2_type)
    print("okay")
    name['경도'] = result[:, 0]
    name['위도'] = result[:, 1]
    
    return name

food1 = data_processing(food1)
food2 = data_processing(food2)
food3 = data_processing(food3)
food4 = data_processing(food4)
food5 = data_processing(food5)
food6 = data_processing(food6)
food7 = data_processing(food7)

food1.to_csv('POI/식품/' + food_name[0] + '.csv', encoding='cp949')
food2.to_csv('POI/식품/' + food_name[1] + '.csv', encoding='cp949')
food3.to_csv('POI/식품/' + food_name[2] + '.csv', encoding='cp949')
food4.to_csv('POI/식품/' + food_name[3] + '.csv', encoding='cp949')
food5.to_csv('POI/식품/' + food_name[4] + '.csv', encoding='cp949')
food6.to_csv('POI/식품/' + food_name[5] + '.csv', encoding='cp949')
food7.to_csv('POI/식품/' + food_name[6] + '.csv', encoding='cp949')

# --------------------------------------------------------------------------------------# 
#                                 Check in map                                          #
# --------------------------------------------------------------------------------------# 

# 데이터 100개 랜덤 추출
sample = food1.sample(n=100)

# 지도 중심 좌표 설정
lat_c, lon_c = 37.53165351203043, 126.9974246490573

# Folium 지도 객체 생성
m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

# 마커 생성
for _, row in sample.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker(location=[lat, lon]).add_to(m)