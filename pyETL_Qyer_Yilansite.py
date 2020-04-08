import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json
from pprint import pprint

# 製作/存取儲存路徑
information_path = r'./Yilan_Qyer'
if not os.path.exists(information_path) :
    os.mkdir(information_path)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
request_url = 'https://place.qyer.com/poi.php?action=list_json'

post_data = {'page': '1',
'type': 'city',
'pid': '9815',
'sort': '32',
'subsort': 'all',
'isnominate': '-1',
'haslastm': 'false',
'rank': '6'}

res = requests.post(url=request_url, headers=headers, data=post_data)     # 窮遊台北景點requests網址
j_data = json.loads(res.text)     # 請求以json格式得到資訊(窮遊是以javascript語言寫成網站)
# pprint(j_data)

for i in range(1,43) :     # 標題頁面1至42頁
    post_data['page'] = i     # postdata頁面參數
    res = requests.post(url=request_url, headers=headers, data=post_data)
    # soup = BeautifulSoup(res.text, 'html.parser')
    j_data = json.loads(res.text)
    try :
        titles = j_data['data']['list'][0]['cnname']     # 標題
    except :
        pass
    for j in range(0,15) :
        try :
            each_article_title = j_data['data']['list'][j]['cnname']     # 標題擷取
            print(each_article_title)
            each_article_grade = j_data['data']['list'][j]['grade']     # 評分
            print('grade: ', each_article_grade)
            each_article_url = 'http:' + j_data['data']['list'][j]['url']     # 標題連結網址
            print(each_article_url)
            # each_title_id = j_data['data']['list'][j]['id']
            # print(each_title_id)
            req = requests.get(each_article_url, headers=headers)
            each_soup = BeautifulSoup(req.text, 'html.parser')     # 標題內網頁內容解析
        except :
            pass
        try :
            each_article_content = each_soup.select('#app > div > div.q-container > div > div.main-bg > div > div.compo-main > div.compo-detail-info > div.poi-detail > div > p')[0].text     # 標題主頁內容
            print(each_article_content)
            publish_time = each_soup.select('#app > div > div.q-container > div > div.main-bg > div > div.compo-main > div.compo-detail-info > div.poi-date > span')[0].text     # 文章更新時間
            time = publish_time.strip().split('\n')[0]
            update_time = time[7:-1].strip('[').strip(']')
            # print(type(time))
            print('更新時間: ', update_time)
            each_location = each_soup.select('#app > div > div.q-container > div > div.main-bg > div > div.compo-main > div.compo-detail-info > ul > li:nth-child(1) > div > p')[0].text     # 景點網址
            print('地址: ', each_location)
        except :
            pass
        try :
            poiid = j_data['data']['list'][j]['id']     # 留言評論postdata變換參數(不同標題不同poiid)
            comment_url = 'https://place.qyer.com/poi.php?action=comment&page=2&order=5&poiid={}&starLevel=all'.format(poiid)     # 留言評論request網址
            comment_post = {
                'action': 'comment',
                'page': '1',
                'order': '5',
                'poiid': '100939',
                'starLevel': 'all'
            }
            comments_detail = []
            for k in range(0,11) :     # 每頁有10則留言
                comment_post['poiid'] = poiid     # 置換參數
                comment_post['page'] = str(k)     # 頁面參數
                comment_req = requests.post(url=comment_url, headers=headers, data=comment_post)
                comment_jsondata = json.loads(comment_req.text)
                try :
                    comments = comment_jsondata['data']['lists'][k]['content']
                    # print('留言: ', comments)
                    comments_string = '"' + comments + '"'
                    # print(comments_string)
                except :
                    pass
                comments_detail.append(comments_string)
            print('留言: ', comments_detail)
        except :
            pass
            # All_comments = dict(enumerate(comments))
            # print(All_comments)
        # all_article_comment = each_soup.select('div[class="comment clearfix"] p')
        # for each_article_comment in all_article_comment :
        #     print(each_article_comment.text)
        # article_detail = each_article_title
        # article_detail += each_article_grade
        # article_detail += each_article_url
        # article_detail += each_article_content
        # article_detail += '地址: ' + each_location
        print("===========================================================================================================================================")

        # article_data = '{' + '文章網址: ' + each_article_url + ', ' + '\n'
        # article_data += '發文時間: ' + update_time + ', ' + '\n'
        # article_data += '標題: ' + each_article_title + ', ' + '\n'
        # article_data += '評分: ' + each_article_grade + ', ' + '\n'
        # article_data += '景點名稱: ' + each_article_title + ', ' + '\n'
        # article_data += '文章內容: ' + each_article_content + ', ' + '\n'
        # article_data += '留言: ' + str(comments_detail) + ', ' + '\n'
        # article_data += '地址: ' + each_location + ', ' + '\n'
        # article_data += '縣市: ' + '宜蘭縣' + ', ' + '\n'
        # article_data += '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------}'
        # article_jdata = json.dumps(article_data, ensure_ascii=False)

        all_keys = {'文章網址', '發文時間', '標題', '評分', '景點名稱', '文章內容', '留言', '地址', '縣市'}
        all_values = {each_article_url, update_time, each_article_title, each_article_grade, each_article_title,
                      each_article_content, str(comments_detail), each_location, '宜蘭縣'}
        Yilan_site_info = dict(zip(all_keys, all_values))
        js_info = json.dumps(Yilan_site_info, ensure_ascii=False)

        with open(r'./Yilan_Qyer/Yilan_site.txt', 'a', encoding='utf-8') as w :
            w.write(js_info)