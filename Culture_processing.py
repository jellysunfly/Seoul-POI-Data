import sys, os
import numpy as np
import pandas as pd
import pyproj
import folium

os.chdir('C:/Users/User/Desktop/Please_give_me_a_chance/POI/POI')

culture1 = pd.read_csv("POI_Ori/문화/fulldata_03_06_01_P_공연장.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture2 = pd.read_csv("POI_Ori/문화/fulldata_03_07_01_P_관광궤도업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture3 = pd.read_csv("POI_Ori/문화/fulldata_03_07_04_P_국제회의시설업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture4 = pd.read_csv("POI_Ori/문화/fulldata_03_07_05_P_박물관,미술관.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture5 = pd.read_csv("POI_Ori/문화/fulldata_03_07_10_P_전문휴양업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture6 = pd.read_csv("POI_Ori/문화/fulldata_03_07_11_P_전통사찰.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture7 = pd.read_csv("POI_Ori/문화/fulldata_03_07_12_P_종합유원시설업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture8 = pd.read_csv("POI_Ori/문화/fulldata_03_07_13_P_종합휴양업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture9 = pd.read_csv("POI_Ori/문화/fulldata_03_11_01_P_관광숙박업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture10 = pd.read_csv("POI_Ori/문화/fulldata_03_11_02_P_관광펜션업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture11 = pd.read_csv("POI_Ori/문화/fulldata_03_11_05_P_자동차야영장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture12 = pd.read_csv("POI_Ori/문화/fulldata_03_11_07_P_일반야영장업.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])
culture13 = pd.read_csv("POI_Ori/문화/fulldata_03_13_02_P_영화상영관.csv", encoding='cp949', usecols=['개방서비스명', '영업상태명', '소재지전체주소', '좌표정보(x)', '좌표정보(y)'])

culture_num = ['culture1', 'culture2', 'culture3', 'culture4', 'culture5', 'culture6', 'culture7', 'culture8', 'culture9', 'culture10', 'culture11', 'culture12', 'culture13']
culture_name = ['공연장', '관광궤도업', '국제회의시설업', '박물관,미술관', '전문휴양업', '전통사찰', '종합유원시설업', '종합휴양업', '관광숙박업', '관광펜션업', '자동차야영자업', '일반야영장업', '영화상영관']

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

culture1 = data_processing(culture1)
culture2 = data_processing(culture2)
culture3 = data_processing(culture3)
culture4 = data_processing(culture4)
culture5 = data_processing(culture5)
culture6 = data_processing(culture6)
culture7 = data_processing(culture7)
culture8 = data_processing(culture8)
culture9 = data_processing(culture9)
culture10 = data_processing(culture10)
culture11 = data_processing(culture11)
culture12 = data_processing(culture12)
culture13 = data_processing(culture13)

culture1.to_csv('POI/문화/' + culture_name[0] + '.csv', encoding='cp949')
culture2.to_csv('POI/문화/' + culture_name[1] + '.csv', encoding='cp949')
culture3.to_csv('POI/문화/' + culture_name[2] + '.csv', encoding='cp949')
culture4.to_csv('POI/문화/' + culture_name[3] + '.csv', encoding='cp949')
culture5.to_csv('POI/문화/' + culture_name[4] + '.csv', encoding='cp949')
culture6.to_csv('POI/문화/' + culture_name[5] + '.csv', encoding='cp949')
culture7.to_csv('POI/문화/' + culture_name[6] + '.csv', encoding='cp949')
culture8.to_csv('POI/문화/' + culture_name[7] + '.csv', encoding='cp949')
culture9.to_csv('POI/문화/' + culture_name[8] + '.csv', encoding='cp949')
culture10.to_csv('POI/문화/' + culture_name[9] + '.csv', encoding='cp949')
culture11.to_csv('POI/문화/' + culture_name[10] + '.csv', encoding='cp949')
culture12.to_csv('POI/문화/' + culture_name[11] + '.csv', encoding='cp949')
culture13.to_csv('POI/문화/' + culture_name[12] + '.csv', encoding='cp949')

# --------------------------------------------------------------------------------------# 
#                                 Check in map                                          #
# --------------------------------------------------------------------------------------# 

'''
# 데이터 100개 랜덤 추출
sample = culture1.sample(n=100)

# 지도 중심 좌표 설정
lat_c, lon_c = 37.53165351203043, 126.9974246490573

# Folium 지도 객체 생성
m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

# 마커 생성
for _, row in sample.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker(location=[lat, lon]).add_to(m)
'''