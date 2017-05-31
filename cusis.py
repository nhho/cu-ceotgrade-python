sid = '1155012345'
pw = 'my password'
bot_token = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
chat_id = '234567890'
loop_sec = 60

import requests
import telepot
import time
import traceback

main_url = 'https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL'
login_slt = '<input name="Submit" type="submit" class="psloginbutton" value="Sign In" onclick="submitAction(document.login)">'
login_url = 'https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?cmd=login&languageCd=ENG'
term_slt = '<a name=\'DERIVED_SSS_SCT_SSR_PB_GO\' id=\'DERIVED_SSS_SCT_SSR_PB_GO\''
term_name_slt = '<span  class=\'PSEDITBOX_DISPONLY\' >'
icsid_slt = '<input type=\'hidden\' name=\'ICSID\' value=\''
term_input_slt = '<td align=\'right\' height=\'13\' class=\'PSLEVEL2GRIDROW\' >'
title_slt = 'href="javascript:submitAction_win0(document.win0,\'CLS_LINK$'
grade_slt = '<td align=\'right\'  class=\'PSLEVEL1GRID*ROW\' >\n<span  class=\'PABOLDTEXT\' >'

db = {}

ses = requests.Session()
while True :
	try :
		html = ses.get(main_url).text
		if html.find(login_slt) != -1 :
			print('login')
			html = ses.post(login_url, data = {
				'timezoneOffset': '-480',
				'userid': sid, 'pwd': pw }).text
			if html.find(login_slt) != -1 :
				raise Exception('Login failed')
		if html.find(term_slt) == -1 :
			raise Exception('No term to select')
		icsid_at = html.find(icsid_slt)
		if icsid_at == -1 :
			raise Exception('No icsid')
		icsid_at += len(icsid_slt)
		icsid = html[icsid_at:html.find('\'', icsid_at)]
		term_no = html.count(term_input_slt)
		term = 0
		while True :
			term_at = html.find(term_input_slt)
			if term_at == -1 :
				break
			html = html[term_at:]
			html = html[html.find(term_name_slt) + len(term_name_slt):]
			term_name = html[:html.find('<')]
			html_new = ses.post(main_url, data = {
				'ICType': 'Panel',
				'ICElementNum': '0',
				'ICStateNum': '1',
				'ICAction': 'DERIVED_SSS_SCT_SSR_PB_GO',
				'ICXPos': '0',
				'ICYPos': '0',
				'ICFocus': '',
				'ICSaveWarningFilter': '0',
				'ICChanged': '-1',
				'ICResubmit': '0',
				'ICSID': icsid,
				'#ICDataLang': 'ENG',
				'SSR_DUMMY_RECV1$sels$0': term}).text
			term += 1
			oe = 'ODD'
			while True :
				title_at = html_new.find(title_slt)
				if title_at == -1 :
					break
				html_new = html_new[title_at:]
				title = html_new[html_new.find('>') + 1:html_new.find('<')]
				grade_slt_oe = grade_slt.replace('*', oe)
				if oe == 'ODD' :
					oe = 'EVEN'
				else :
					oe = 'ODD'
				html_new = html_new[html_new.find(grade_slt_oe) + len(grade_slt_oe):]
				grade = html_new[:html_new.find('<')].replace('&nbsp;', '_')
				if (term_name, title) not in db :
					db[(term_name, title)] = ''
				if db[(term_name, title)] != grade :
					db[(term_name, title)] = grade
					bot = telepot.Bot(bot_token)
					bot.sendMessage(chat_id, '%s %s: %s' % (term_name, title, grade))
	except :
		print(traceback.format_exc())
	time.sleep(loop_sec)
