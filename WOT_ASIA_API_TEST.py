import pandas as pd
from pandas import json_normalize
import requests
from datetime import datetime
from tabulate import tabulate


print('''World of Tanks CLAN API Tester\
 Version 1.0

Made by PangPangGod

''')

#검색 만들어서 여러 개중에 선택하고 clan_id 저장하기

search_tag = input("Type CLAN Tag or Description next to it. >> ")

session = requests.get('https://api.worldoftanks.asia/wot/clans/list/?application_id=<APPLICATION_ID>&search={}'.format(search_tag))
df = json_normalize(session.json()["data"])

#오류 처리
try : df_adj=df.loc[:,['tag','name']]
except KeyError :
    print('검색한 결과가 없습니다. 프로그램을 다시 실행해주세요')
    exit()

df_adj.index=df_adj.index+1
print("Hey! There's multiple ouput from your search. including:\n")
print(tabulate(df_adj, headers='keys', tablefmt='psql'))
val = int(input('\n출력한 결과를 숫자로 선택하세요(EX: 1) >> '))
val = df_adj.loc[val,'tag']
clan_id = int(df[df['tag']==val]['clan_id'])

#clan id로 멤버 정보 가져오기
session2 = requests.get('https://api.worldoftanks.asia/wot/clans/info/?application_id=<APPLICATION_ID>&clan_id={}&language=ko'.format(clan_id))

ob = json_normalize(session2.json()['data'][str(clan_id)],'members')

temp_list = list(ob['account_id'])
temp_list = list(map(str,temp_list))

long_string = '%2C'.join(temp_list)

#멤버 정보들에 들어있는 id 번호를 통해 list를 만들고 플레이어 정보 긁어와서 rating, 로그아웃 시간 추적해서 결과 내놓기.

session3 = requests.get('https://api.worldoftanks.asia/wot/account/info/?application_id=<APPLICATION_ID>&account_id={}&language=en'.format(long_string))
tp1,tp2,tp3 = [],[],[]

for id_num in temp_list :
    ec = json_normalize(session3.json()['data'][id_num])
    tp1.append(ec['global_rating'][0])
    tp2.append(ec['nickname'][0])
    tp3.append(datetime.fromtimestamp(ec['logout_at'][0]))

tp4 = {'nickname':tp2,'global_rating':tp1,'logout_at':tp3}

#tp4 변수를 통해 최종 DataFrame 만들고 출력하기.
final_df = pd.DataFrame(tp4)
final_df.index = final_df.index+1
final_df = final_df.sort_values(by='logout_at',ascending=False)
print(tabulate(final_df, headers='keys', tablefmt='psql'))

session.close();session2.close();session3.close()

