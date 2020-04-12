import requests
from bs4 import BeautifulSoup
import re
import time
import json
from selenium.webdriver import Chrome
from selenium import webdriver
import os
from pprint import pprint
import datetime

data_path = r'./hotels_com'
if not os.path.exists(data_path) :
    os.mkdir(data_path)

# browser = Chrome(r'./chromedriver.exe')

# ===網頁滾動指令===
driver = webdriver.Chrome()
driver.implicitly_wait(3)

today_date = datetime.date.today()
start_date = today_date + datetime.timedelta(days=1)
end_date = today_date + datetime.timedelta(days=2)
print(today_date, start_date, end_date)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
url = 'https://tw.hotels.com/search.do?resolved-location=CITY%3A1726364%3AUNKNOWN%3AUNKNOWN&destination-id=1726364&q-destination=%E5%AE%9C%E8%98%AD%E7%B8%A3,%20%E5%8F%B0%E7%81%A3&q-check-in={}&q-check-out={}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'.format(start_date, end_date)


# start_time = '2020-04-06'
# end_time = '2020-04-07'
# url = 'https://tw.hotels.com/search.do?resolved-location=CITY%3A1366745%3AUNKNOWN%3AUNKNOWN&destination-id=1366745&q-destination=%E5%8F%B0%E5%8C%97,%20%E5%8F%B0%E7%81%A3&q-check-in={}&q-check-out={}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'.format(start_time, end_time)

# pay_load = {'AQB=1&ndh=1&pf=1&t=5%2F3%2F2020%2021%3A44%3A46%200%20-480&mid=86854823063100973194593750661374596059&aamlh=11&ce=UTF-8&ns=hotelscom&cdp=2&pageName=search%20result%20with%20dates&g=https%3A%2F%2Ftw.hotels.com%2Fsearch.do%3Fresolved-location%3DCITY%253A1366745%253AUNKNOWN%253AUNKNOWN%26destination-id%3D1366745%26q-destination%3D%25E5%258F%25B0%25E5%258C%2597%2C%2520%25E5%258F%25B0%25E7%2581%25A3%26q-check-in%3D2020-04-10%26q-check-out%3D2020-04-11%26q-rooms%3D1%26q-room-0-adults%3D2%26q-room-0-children%3D0&r=https%3A%2F%2Ftw.hotels.com%2F&cc=TWD&ch=Results%20%3A%20List&server=tw.hotels.com&events=event33&products=LOCAL%3B6894398%2CMULTISOURCE%3B18620961%2CLOCAL%3B18266352&aamb=RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y&v1=city%7Csrs%7Cunknown%7CAutoR%3A%3Acity&c2=UBS&v2=%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3&c3=%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3&v3=2%7C0&l3=D%3Dv34&c4=1%7C1-8%7C1%7C1%7C65&v4=%7CSI%3Aanonymous%7CVS%3AreturnVisitor%7CHCR%3AnotApplicable%7CFC%3AnotApplicable%7CNS%3Aunknown%7CTI%3AnotApplicable%7CSM%3AnotApplicable%7CIR%3Aanonymous%7C&c5=251462&v5=1&v6=1366745&c7=1623&v7=5&c8=0&v8=1&c9=1647&v9=UBS&c11=1647%7Cna%7Cna%7Cna%7Cna&v13=251462&c14=D%3Dv7&c15=1&c17=PB%20-%200%7CEA%20-%200%7CEA%20IN%20-%200%7CEA%20OUT%20-%200&c18=D%3Dv6&c19=1&c20=2&c21=0&v22=1%7CTWD%7C24%3A444308%3A1731.6000%3A865.8000%3A0%7C24%3A699887%3A2813.8500%3A2532.4600%3A1%7C24%3A698854%3A%3A%3A0%7C24%3A438115%3A1021.48%3A848.4800%3A0%7C24%3A347537%3A2162.6000%3A865.0400%3A1&v23=1%7CTWD%7C24%3A434223%3A1878.7900%3A1233.6100%3A1%7C24%3A973659584%3A1887.4500%3A717.2300%3A1%7C24%3A1553209344%3A1443.1200%3A1183.3600%3A1%7C24%3A460813%3A692.6400%3A658.0100%3A1%7C24%3A682854592%3A2165.95%3A1108.2300%3A0&v24=MCTC%3DNULL%3BTU%3DNA%3BPDID%3DNULL%3BMVT%3D&v26=TW%3A%3ATAIPEI%3A&c27=0531e132-c629-4dde-9e70-16c357affa7b&c28=0&c29=D%3Dv42&c30=city%7Csrs%7Cunknown%7CAutoR%3A%3Acity&c32=D%3Dv43&c33=D%3Dv33&v33=search%20result%20with%20dates&c34=2020.4.8645&v34=H98%3A031.006%2CH1423%3A009.099%2CH1871%3A007.002%2CH2522%3A007.001%2CH4154%3A004.002%2CH4170%3A003.001%2CH4516%3A001.000%2CH4517%3A001.000%2CH4518%3A003.000%2CH4519.0%2CH4532%3A004.001%2CM376%3A131.047%2CM904%3A000.000%2CM1167%3A000.000%2CM1291%3A011.002%2CM1292%3A004.001%2CM1293%3A037.000%2CM1294%3A036.025%2CM3736%3A000.000%2CM4200%3A008.001%2CM4440%3A005.002%2CM4869%3A001.000%2CM4952%3A019.000%2CM4961%3A001.000%2CM5167%3A001.000%2CM5342%3A000.000%2CM5663%3A000.000%2CM6184%3A000.000%2CM6388%3A002.000%2CM6476%3A000.000%2CM6775%3A000.000%2CM6779%3A000.000%2CM6890%3A001.000%2CM6990%3A001.000%2CM7015%3A007.001%2CM7036%3A000.000%2CM7066%3A000.000%2CM7192%3A005.001%2CM7214%3A000.000%2CM7215%3A009.001%2CM7296%3A000.000%2CM7305%3A002.002%2CM7306%3A002.002%2CM7353%3A010.001%2CM7362%3A000.000%2CM7384%3A000.000%2CM7433%3A004.001%2CM7552%3A023.001%2CM7561%3A000.000%2CM7576%3A000.000%2CM7763%3A000.000%2CM7855%3A008.001%2CM7867%3A000.000%2CM7870%3A000.000%2CM7895%3A000.000%2CM8039%3A008.002%2CM8065%3A013.001%2CM8130%3A009.001%2CM8258%3A011.002%2CM8272%3A000.000%2CM8287%3A000.000%2CM8336%3A010.002%2CM8347%3A011.002%2CM8405%3A008.001%2CM8434%3A000.000%2CM8448%3A102.000%2CM8483%3A000.000%2CM8485%3A000.000%2CM8625%3A002.002%2CM8692%3A008.002%2CM8693%3A000.000%2CM8698%3A000.000%2CM8708%3A000.000%2CM8714%3A000.000%2CM8718%3A000.000%2CM8758%3A000.000%2CM8915%3A000.000%2CM8952%3A000.000%2CM8976%3A000.000%2CM8992%3A001.002%2CM9004%3A000.000%2CM9035%3A001.001%2CM9065%3A003.003%2CM9066%3A004.001%2CM9117%3A000.000%2CM9173%3A000.000%2CM9207%3A000.000%2CM9250%3A000.000%2CM9255%3A002.001%2CM9281%3A000.000%2CM9282%3A000.000%2CM9424%3A001.002%2CM9431%3A002.001%2CM9434%3A001.001%2CM9491%3A002.001%2CM8738%3A000.000%2CM7666%3A000.000%2CM8072%3A000.000%2CM8836%3A000.000%2CM7905%3A005.003%2CM8894%3A000.000%2CM9444%3A000.000%2CM9100%3A000.000%2CM7625%3A000.000%2CM8037%3A000.000%2CM8691%3A001.001%2CM5104%3A001.000%2CM8410%3A000.003%2CM8425%3A006.001%2CM8115%3A009.001%2CM8235%3A000.000%2CM5979%3A000.000%2CM8743%3A000.000%2CM7861%3A025.003%2CM6442%3A000.000%2CM8204%3A000.000%2CM7115%3A000.000%2CM9461%3A001.001%2CM7500%3A000.000%2CM8400%3A006.001%2CM6039%3A001.000%2CM5349%3A001.000%2CM6946%3A000.000%2CM7440%3A000.000%2CM7858%3A000.000%2CM6549%3A000.000%2CM8056%3A004.001%2CM7108%3A000.000%2CM4969%3A001.000%2CM8477%3A000.000%2CM8592%3A000.000%2CM7871%3A000.000%2CM6425%3A000.002%2CM6574%3A000.000%2CM7950%3A000.000%2CM9145%3A001.000%2CM9197%3A000.000&v35=city%7Csrs%7Cunknown%7CAutoR%3A%3Acity%7CSearchResultPage%7CC%7CL%7CT%7CH%7C%7C1366745&c36=%7CSI%3Aanonymous%7CVS%3AreturnVisitor%7CHCR%3AnotApplicable%7CFC%3AnotApplicable%7CNS%3Aunknown%7CTI%3AnotApplicable%7CSM%3AnotApplicable%7CIR%3Aanonymous%7C&c38=not%20signed%20in&c39=not%20signed%20in&v41=TWD&v42=5%7C1%7C20200410%7C20200411&v43=zh_TW%7CHCOM_TW%7Ctw.hotels.com&c46=D%3Dv61&v49=1366745%3AA%3A1000000000000003518%3A327630-B%3A1000000000000003518%3A327630%3A904.0%3AN&c50=hermom06&c54=SRP%20%7C%20dd%20not%20%7C%20dd%20not%20shown%20%7C%200&c55=Search%3A%3ASearchResultPage%7CAutoR%3A%3Acity%7C%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3&c57=DD%20CTA%20S&v59=Desktop%7Csearch%20result%20with%20dates%7C5%7CNA&c60=search%20result%20with%20dates%20%3A%3A%20Worldspan%20%3A%3A%20no%20%3A%3A%200%20%3A%3A%201%7C1-8%7C1%7C1%7C65&v61=Desktop&v63=22883f78-2cbf-4dec-a262-a038d645d1f0&c64=DOD%2CCompression%20message%20shown&c67=search%20result%20with%20dates%20%3A%3A%20PKG%20%3A%3A%20H%20%3A%3A%20NA&c74=search%20result%20with%20dates%20%7C%20ms%20shown%20%7C%20N&v81=SRP%20%7C%20MRP%20-%20N%20%7C%20MS%20-%200%20%7C%20V2%20-%200%20%7C%20V3%20-%200%20%7C%20SV%20-%200&v84=VisitorAPI%20Present&v93=aws.us-west-2.unknown&v95=Unknown&v98=search%20result%20with%20dates%20%3A%3A%20No%20Earn%20Property%20Seen%20%3A%3A%20True&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1241&bh=920&AQE=1'}
req = requests.get(url, headers=headers)
# soup = BeautifulSoup(req.text, 'html.parser')
# print(soup.prettify())


driver.get(url=url)
for page in range(1, 500):     # 模擬滾動500次
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)     # 滾動後停留3秒讓網頁load近來

# -----從頭滾到尾-----
# js1 = 'return document.body.scrollHeight'
# js2 = 'window.scrollTo(0, document.body.scrollHeight)'
# old_scroll_height = 0
# while browser.execute_script(js1) >= old_scroll_height:
#     old_scroll_height = browser.execute_script(js1)
#     browser.execute_script(js2)
#     time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

titles = soup.select('div[class="description resp-module"] h3 a')
data_content =[]
for i, title in enumerate(titles) :
    print(title.text)
    location = soup.select('address[class="contact"] span')[i].text
    try :
        grade = soup.select('div[class="reviews-box resp-module"] strong')[i].text
    except :
        pass
    level = soup.select('div[class="additional-details resp-module"] span')[i].text
    link = 'https://tw.' + soup.select('div[class="description resp-module"] h3 a')[i]['href'].strip('/')
    print('地址: ', location)
    print('評價: ', grade)
    # print('星等: ', level)
    print('網址 : ', link)
    print('===============================================================================================================================================================================================')

    grade_f = re.findall(r'\d+\.?\d', grade)[0]  # 使用正規表示式並取出list中的評分項目

    js_data = {'酒店名稱': title.text,
               '酒店地址': location,
               '酒店評分': grade_f,
               '縣市': '宜蘭縣',
               '網址': link,
               '留言': 'NA'}

    json_data = json.dumps(js_data, ensure_ascii=False)
    with open(r'./hotels_com/HC_Yilan/hotelcom_Yilan.json', 'a', encoding='utf-8') as w:
        w.write(json_data + '-----')

    with open(r'./hotels_com/HC_Yilan/hotelscom_Yilan_%s.txt' % (title.text), 'a', encoding='utf-8') as t:
        t.write(json_data)