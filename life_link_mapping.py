import pandas as pd
import numpy as np
import haversine as hs
import os, sys
import csv

df = pd.read_csv('link_seoul_ver3.csv', encoding='cp949')
link = df['LINK_ID'].values
geometry = df['geometry']

geometry = geometry.str.replace('LINESTRING', '')
geometry = geometry.str.replace('(', '')
geometry = geometry.str.replace(')', '')
geometry = geometry.str.replace(' ', ',')
geometry = geometry.str.replace(',,', ',')
geometry = geometry.str.split(',')
for i in range(len(geometry)):
    geometry[i].pop(0)


def distance(line_x1, line_y1, line_x2, line_y2, point_x, point_y):
    ab = np.array([line_x2 - line_x1, line_y2 - line_y1])
    ac = np.array([point_x - line_x1, point_y - line_y1])
    result = np.array([line_x1, line_y1]) + ab * (np.dot(ab, ac) / np.dot(ab, ab))
    return hs.haversine((point_x, point_y), (result[0], result[1]))


'''
def distance(x1, y1, x2, y2, x3, y3):
    if x1 == x2:
        m = 0
    else:
        m = (y2 - y1) / (x2 - x1)
    a = m
    b = -1
    c = y1 - m * x1
    d = abs(a * x3 + b * y3 + c) / np.sqrt(a ** 2 + b ** 2)
    return d
'''


def distance_link(link, geometry, x, y):
    d = []
    for i in range(0, len(geometry[link]) - 2, 2):
        x1 = float(geometry[link][i + 1])
        y1 = float(geometry[link][i])
        x2 = float(geometry[link][i + 3])
        y2 = float(geometry[link][i + 2])
        d.append(distance(x1, y1, x2, y2, x, y))
    return min(d)


def distance_haversine(link, geometry, x, y):
    for i in range(len(geometry[link])):
        if i % 2 == 0:
            x1 = float(geometry[link][i + 1])
            y1 = float(geometry[link][i])
            if hs.haversine((x, y), (x1, y1)) <= 0.2:
                return True
            else:
                continue
        else:
            continue


def link_haversine(geometry, x, y):
    link_haversine = []
    for i in range(len(geometry)):
        if distance_haversine(i, geometry, x, y):
            link_haversine.append(i)
    return link_haversine


def link_shortest(link_haversine, geometry, x, y):
    d = []
    for i in range(len(link_haversine)):
        d.append(distance_link(link_haversine[i], geometry, x, y))
    if len(d) == 0:
        return None
    else:
        return link_haversine[d.index(min(d))]


def mapping_link(x, y):
    linked_haversine = link_haversine(geometry, x, y)
    return link_shortest(linked_haversine, geometry, x, y)


def indexToLink(index: int) -> int:
    return int(df.iloc[index]["LINK_ID"])

def save_result(data):
    data = data.drop('Unnamed: 0', axis=1)
    data_list = []

    for idx in range(len(data)):
        link_id = mapping_link(data.iloc[idx, 6], data.iloc[idx, 5])

        if link_id is None:
            link_id = np.nan

        else:
            link_id = indexToLink(link_id)
        
        data_list.append(link_id)

    data["LINK"] = data_list
    data = data.dropna(axis=0)

    return data


# loc1 = (37.547871, 126.997193)
# print(mapping_link(loc1[0],loc1[1]))
# 입력은 위경도

life1 = pd.read_csv("POI/생활/골프연습장업.csv", encoding='cp949')
life2 = pd.read_csv("POI/생활/골프장.csv", encoding='cp949')
life3 = pd.read_csv("POI/생활/대규모점포.csv", encoding='cp949')
life4 = pd.read_csv("POI/생활/등록체육시설업.csv", encoding='cp949')
life5 = pd.read_csv("POI/생활/목욕장업.csv", encoding='cp949')
life6 = pd.read_csv("POI/생활/방문판매업.csv", encoding='cp949')
life7 = pd.read_csv("POI/생활/빙상장업.csv", encoding='cp949')
life8 = pd.read_csv("POI/생활/수영장업.csv", encoding='cp949')
life9 = pd.read_csv("POI/생활/스키장.csv", encoding='cp949')
life10 = pd.read_csv("POI/생활/썰매장업.csv", encoding='cp949')
life11 = pd.read_csv("POI/생활/종합체육시설업.csv", encoding='cp949')
life12 = pd.read_csv("POI/생활/체력단련장업.csv", encoding='cp949')
life13 = pd.read_csv("POI/생활/통신판매업.csv", encoding='cp949')


life1 = save_result(life1)
life2 = save_result(life2)
life3 = save_result(life3)
life4 = save_result(life4)
life5 = save_result(life5)
life6 = save_result(life6)
life7 = save_result(life7)
life8 = save_result(life8)
life9 = save_result(life9)
life10 = save_result(life10)
life11 = save_result(life11)
life12 = save_result(life12)
life13 = save_result(life13)

life1.to_csv("POI/생활/골프연습장업_link.csv", encoding='cp949')
life2.to_csv("POI/생활/골프장_link.csv", encoding='cp949')
life3.to_csv("POI/생활/대규모점포_link.csv", encoding='cp949')
life4.to_csv("POI/생활/등록체육시설업_link.csv", encoding='cp949')
life5.to_csv("POI/생활/목욕장업_link.csv", encoding='cp949')
life6.to_csv("POI/생활/방문판매업_link.csv", encoding='cp949')
life7.to_csv("POI/생활/빙상장업_link.csv", encoding='cp949')
life8.to_csv("POI/생활/수영장업_link.csv", encoding='cp949')
life9.to_csv("POI/생활/스키장_link.csv", encoding='cp949')
life10.to_csv("POI/생활/썰매장업_link.csv", encoding='cp949')
life11.to_csv("POI/생활/종합체육시설업_link.csv", encoding='cp949')
life12.to_csv("POI/생활/체력단련장업_link.csv", encoding='cp949')
life13.to_csv("POI/생활/통신판매업_link.csv", encoding='cp949')