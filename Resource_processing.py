import sys, os
import numpy as np
import pandas as pd
import pyproj
import folium

os.chdir('C:/Users/User/Desktop/Please_give_me_a_chance/POI/POI')

resource1 = pd.read_csv("POI_Ori/자원환경/fulldata_09_28_08_P_석유판매업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])

resource_num = ['resource1']
resource_name = ['석유판매업']

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

resource1 = data_processing(resource1)

resource1.to_csv('POI/자원환경/' + resource_name[0] + '.csv', encoding='cp949')

# --------------------------------------------------------------------------------------# 
#                                 Check in map                                          #
# --------------------------------------------------------------------------------------# 

# 데이터 100개 랜덤 추출
sample = resource1.sample(n=100)

# 지도 중심 좌표 설정
lat_c, lon_c = 37.53165351203043, 126.9974246490573

# Folium 지도 객체 생성
m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

# 마커 생성
for _, row in sample.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker(location=[lat, lon]).add_to(m)