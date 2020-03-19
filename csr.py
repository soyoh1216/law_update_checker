import requests
import re
from bs4 import BeautifulSoup
import csv
from kanjize import kanji2int
from datetime import datetime

# 会社法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=417AC0000000086
# 法人税法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=340AC0000000034
# 個人情報保護法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=415AC0000000057
# 特定商取引法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=351AC0000000057
# 消費者契約法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=412AC0000000061
# 景品表示法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=337AC0000000134
# 労働基準法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=322AC0000000049
# 派遣法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=360AC0000000088
# 下請法	https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=331AC0000000120


def getTxt(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	latestUpdate = soup.find(text=re.compile("最終更新："))
	#latestUpdate.replace('\u3000', '')
	splitedTxt = latestUpdate.split("：")

	return splitedTxt[1].replace('\u3000', '')

def getJpDate(jp):
	jpDate = jp.split("公布")
	jpDate = jpDate[0]
	return jpDate

# yyyymm.csv を作って書き出し
def createFile(val):
	now_time = datetime.now()
	now_time = now_time.strftime('%Y%m')
	with open(now_time + ".csv", 'w', newline='') as w:
		writer = csv.writer(w)
		writer.writerows(val)

with open('laws_test.csv', 'r') as f:
	reader = csv.reader(f)
	# 日付変換するなら使うかも
	# print(kanji2int("平成三十一年"))
	
	val = []
	for rd in reader:
		latestUpdate = getTxt(rd[1])
		val.append([rd[0] + "," + getJpDate(latestUpdate)])
	
	# 	print(rd[0] + "," + latestUpdate)
		
	# この形にしたい val = [['a','123'],['b','567']]
	# val.append(['a','123'])
	# val.append(['b','567'])
	print(val)
	createFile(val)
	#createFile(rd[0] + "," + latestUpdate)
