import requests
from bs4 import BeautifulSoup as BS
import time
import re
import json
from docx import Document

#headers = {}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

cookies = dict(cookies_are='working')

urltg = 'https://tangorin.com'
urlhj = 'https://dict.hjenglish.com/'

def findPart(regex, text): 
	res = re.findall(regex, text)
	str = ''
	for r in res: 
		str = str + r
	return str

def draw_prounce(p):
	txt = str(p)
	g = findPart(u"[(\u30a0-\u30ff)|(\u3040-\u309f)]+", txt)
	return g
###

def list_Header(krm):
	JY = krm.contents[1]
	JLPT = krm.contents[2]
	reading = krm.contents[3]
	meaning = krm.contents[4]
	print(meaning.text)
	for sec in reading:
		e = draw_prounce(sec)
		print(e)
	return

def get_sub_exam(session, a):
	href = a.get("href")
	sub_exam = session.get(urltg+'/api/dict/extra'+href)
	print(sub_exam, sub_exam.url, type(sub_exam))
	#print(sub_exam.text)
	js = json.loads(sub_exam.text)
	print('--------------')
	if (js['jlpt']):
		print('JLPT=', js['jlpt'], type(js['jlpt']))

	print('###########')
	
def list_Example(exp, session):
	dl = exp.dl
	for div in dl:
		dt = div.dt
		dd = div.dd
		a = dt.a
		ruby = dt.ruby
		try:
			print(a.contents[0]+"("+ ruby.contents[0]+")" + dd.contents[0])
		#	get_sub_exam(session, a)
		except Exception as e:
			print(e)
	return


###
def extract_tango(kanji):
	stg = requests.Session()
	payload = {'search':kanji} 
	rtg = stg.get(urltg+"/kanji", headers=headers, params=payload)
	print(rtg.url)

	try:
		soup = BS(rtg.text, "lxml")
		div = soup.body.div.main.section.dl.div
		ddht = div.contents[1]
		list_Header(ddht)
		ddexample = div.contents[4]
		list_Example(ddexample, stg)
	except Exception as e:
		return 0

extract_tango('星')












'''
# post = {('search','訪')}
# rtg = requests.get(urltg, headers=headers)
#r = requests.post(url, data=post)

#rhj = requests.get(urlhj,  headers=headers)
rtg = requests.get(urltg,  headers=headers, cookies=cookies, timeout=1)

print(rtg.headers)

print(rtg.url)
print(rtg.status_code)
#print(rhj.content)
'''
