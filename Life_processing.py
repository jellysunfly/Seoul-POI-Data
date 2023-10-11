import sys, os
import numpy as np
import pandas as pd
import pyproj
import folium

os.chdir('C:/Users/User/Desktop/Please_give_me_a_chance/POI/POI')

life1 = pd.read_csv("POI_Ori/생활/fulldata_08_25_01_P_대규모점포.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life2 = pd.read_csv("POI_Ori/생활/fulldata_08_26_02_P_방문판매업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life3 = pd.read_csv("POI_Ori/생활/fulldata_08_26_04_P_통신판매업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life4 = pd.read_csv("POI_Ori/생활/fulldata_10_31_01_P_골프연습장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life5 = pd.read_csv("POI_Ori/생활/fulldata_10_31_02_P_골프장.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life6 = pd.read_csv("POI_Ori/생활/fulldata_10_31_03_P_등록체육시설업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life7 = pd.read_csv("POI_Ori/생활/fulldata_10_34_01_P_빙상장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life8 = pd.read_csv("POI_Ori/생활/fulldata_10_35_01_P_수영장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life9 = pd.read_csv("POI_Ori/생활/fulldata_10_36_01_P_스키장.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life10 = pd.read_csv("POI_Ori/생활/fulldata_10_37_01_P_종합체육시설업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life11 = pd.read_csv("POI_Ori/생활/fulldata_10_39_01_P_썰매장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life12 = pd.read_csv("POI_Ori/생활/fulldata_10_42_01_P_체력단련장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
life13 = pd.read_csv("POI_Ori/생활/fulldata_11_44_01_P_목욕장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])

life_num = ['life1', 'life2', 'life3', 'life4', 'life5', 'life6', 'life7', 'life8', 'life9', 'life10', 'life11', 'life12', 'life13']
life_name = ['대규모점포', '방문판매업', '통신판매업', '골프연습장업', '골프장', '등록체육시설업', '빙상장업' ,'수영장업', '스키장', '종합체육시설업', '썰매장업', '체력단련장업', '목욕장업']

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

life1 = data_processing(life1)
life2 = data_processing(life2)
life3 = data_processing(life3)
life4 = data_processing(life4)
life5 = data_processing(life5)
life6 = data_processing(life6)
life7 = data_processing(life7)
life8 = data_processing(life8)
life9 = data_processing(life9)
life10 = data_processing(life10)
life11 = data_processing(life11)
life12 = data_processing(life12)
life13 = data_processing(life13)

life1.to_csv('POI/생활/' + life_name[0] + '.csv', encoding='cp949')
life2.to_csv('POI/생활/' + life_name[1] + '.csv', encoding='cp949')
life3.to_csv('POI/생활/' + life_name[2] + '.csv', encoding='cp949')
life4.to_csv('POI/생활/' + life_name[3] + '.csv', encoding='cp949')
life5.to_csv('POI/생활/' + life_name[4] + '.csv', encoding='cp949')
life6.to_csv('POI/생활/' + life_name[5] + '.csv', encoding='cp949')
life7.to_csv('POI/생활/' + life_name[6] + '.csv', encoding='cp949')
life8.to_csv('POI/생활/' + life_name[7] + '.csv', encoding='cp949')
life9.to_csv('POI/생활/' + life_name[8] + '.csv', encoding='cp949')
life10.to_csv('POI/생활/' + life_name[9] + '.csv', encoding='cp949')
life11.to_csv('POI/생활/' + life_name[10] + '.csv', encoding='cp949')
life12.to_csv('POI/생활/' + life_name[11] + '.csv', encoding='cp949')
life13.to_csv('POI/생활/' + life_name[12] + '.csv', encoding='cp949')

# --------------------------------------------------------------------------------------# 
#                                 Check in map                                          #
# --------------------------------------------------------------------------------------# 

# 데이터 100개 랜덤 추출
sample = life1.sample(n=100)

# 지도 중심 좌표 설정
lat_c, lon_c = 37.53165351203043, 126.9974246490573

# Folium 지도 객체 생성
m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

# 마커 생성
for _, row in sample.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker(location=[lat, lon]).add_to(m)