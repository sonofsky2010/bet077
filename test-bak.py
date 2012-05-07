#!/usr/bin/python
import urllib2
from HTMLParser import HTMLParser
import re
from lxml import html

tr_id_patern = re.compile('tr.*')

request_url = 'http://1x2.bet007.com/bet007history.aspx?matchdate='
def fetch(year, month, day):
    fetch_url = request_url + '%d' % year + '-' + '%d' % month + '-' + '%d' % day
    con = urllib2.urlopen(fetch_url)
    ret_array = []
    try:
        data = con.read()
        doc = html.document_fromstring(data)
        table_element = doc.get_element_by_id('table_schedule')
        if table_element == None:
            return None
        trs = table_element.xpath('//tr')
        if len(trs) < 3:
            return None
        for tr in trs[2:]:
            tr_id = tr.get('id')
            if tr_id != None and tr_id[:3] != 'tr2':
                tds = tr.findall('td')
                td_win = tds[4]
                td_draw = tds[5]
                td_lose = tds[6]
                td_result = tds[12]
                td_time = tds[2]
                td_home = tds[3]
                td_away = tds[11]
                win_rate = td_win.text
                draw_rate = td_draw.text
                lose_rate = td_lose.text
                font_result = td_result.find('font')
                match_result = font_result.text
                match_time = td_time.text_content()
                td_home_href = td_home.find('a')
                td_home_iter = td_home_href.itertext()
                td_home_iter.next()
                home_team = td_home_iter.next()
                print home_team
                
#                td_home_font = td_home_href.find('font')
#                if td_home_href != None:
#                    td_home_href.remove(td_home_font)
#                home_team = td_home_href.text_content()
                away_team = td_away.find('a').text
                aDict = {'win':win_rate, 'draw': draw_rate, 'lose': lose_rate, 'result': match_result, 'time': match_time, 'home': home_team, 'away': away_team}
                ret_array.append(aDict)
        return ret_array
    except:
        print sys.exc_info()[0], sys.exc_info()[1]       
    finally:
        return ret_array
ret = fetch(2012, 5, 2)
for aResult in ret:
    print aResult
print len(ret)
