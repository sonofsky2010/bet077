#!/usr/bin/env python
# encoding: utf-8
import urllib2
import sys
import re
from lxml import html
import sqlite3

tr_id_patern = re.compile('tr.*')

request_url = 'http://1x2.bet007.com/bet007history.aspx?matchdate='
db_name = 'result.db'
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
#                td_home = tds[3]
#                td_away = tds[11]
                win_rate = td_win.text
                draw_rate = td_draw.text
                lose_rate = td_lose.text
                font_result = td_result.find('font')
                match_result = font_result.text
                match_time = td_time.text_content()
#                td_home_href = td_home.find('a')
#                home_name = td_home_href.text_content()
#                print home_name
#                home_team = td_home_href.text_content()
#                td_home_font = td_home_href.find('font')
#                if td_home_href != None:
#                    td_home_href.remove(td_home_font)
#                home_team = td_home_href.text_content()
#                away_team = td_away.find('a').text
                aDict = {'win':win_rate, 'draw': draw_rate, 'lose': lose_rate, 'result': match_result, 'time': match_time}
                ret_array.append(aDict)
        return ret_array
    except:
        print sys.exc_info()[0], sys.exc_info()[1]       
    finally:
        return ret_array
def store_results(ret):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for aResult in ret:
        win_rate = float(aResult['win'])
        draw_rate = float(aResult['draw'])
        lose_rate = float(aResult['lose'])
        match_result = aResult['result']
        match_date = aResult['time']
        home_goal = match_result.split('-')[0]
        away_goal = match_result.split('-')[1]
        result = 0
        if home_goal > away_goal:
            result = 3
        elif home_goal == away_goal:
            result = 1
        else:
            result = 0
        c.execute("insert or ignore INTO results VALUES ('%s', %f, %f, %f, %d)" % (match_date, win_rate, draw_rate, lose_rate, result));
        conn.commit()
    c.close()

def main():
    years = [2009, 2010, 2011]
    day_count_dict = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    for year in [2011]:
        for month in [12]:
            day_count = day_count_dict[month]
            for day in [24,25,26,27,28,29,30,31]:
                ret = fetch(year, month, day)
                store_results(ret)
                print "finshed fetched %d-%d-%d" % (year, month, day)

if __name__ == '__main__':
    main()
                
                
        
        


    
