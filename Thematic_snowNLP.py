# pip install elasticsearch
from snownlp import SnowNLP
from snownlp import sentiment
from snownlp import seg
import json

import time
from elasticsearch import Elasticsearch




def connect_elasticsearch():
    global es

    es = Elasticsearch(hosts="192.168.1.137",timeout=30)


def elasticsearch_search(index,query_body,size=50):
    # {"query": {"match": {'酒店地址': '台北'}}}

    es.indices.refresh(index=index)
    res = es.search(index=index,size=size, body=query_body)

    return res['hits']['hits']





'''從elasticsearch 拉目標類別 文章並依序進snownlp 評分 最後加總'''
def elasticsearch_place(each_label):
    connect_elasticsearch()
    query_str =  each_label
    place_list = []
    '''初步找出這類別有哪些推薦景點'''
    for one in elasticsearch_search(index='place_clean_v1', size=50, query_body={"query": {"match": {'文章內容': query_str}}}):

        if one['_source']['景點名稱'] not in place_list: place_list.append(one['_source']['景點名稱'])

    '''將這些景點的文章統整'''
    place_article_dict = {}
    for each_place in place_list :
        for two in elasticsearch_search(index='place_clean_v1', size=100,
                                                         query_body={"query": {"match": {'景點名稱': each_place}}}):

            # if each_place not in place_article_dict:
            #     place_article_dict[each_place] = two['_source']['文章內容']
            # else:
            #     place_article_dict[each_place] += two['_source']['文章內容']


            '''將文章內容只留中文 後 進 snowNLP '''
            article= two['_source']['文章內容']

            if each_place not in place_article_dict:
                place_article_dict[each_place] = article
            else:
                place_article_dict[each_place] += article


    return place_article_dict


def main():
    target_dict = {'古蹟': 'Historic',
                   '海岸': 'coastal',
                   '瀑布': 'waterfall',
                   '燈塔': 'Lighthouse',
                   '登山': 'Mountaineering',
                   '遊樂園': 'amusement_park',
                   '披薩': 'pizza',
                   '火鍋': 'hot_pot',
                   '冰淇淋': 'ice_cream',
                   '墨西哥捲餅': 'burrito',
                   '燒烤': 'rotisserie',
                   '親子': 'Parent_child',
                   '情侶': 'Couple',
                   '老少咸宜': 'Old_and_young',
                   '朋友': 'friend'}

    for key in target_dict.keys() :     # 將tag依序查找
        # print(key)
        dict_tmp = elasticsearch_place('台北 '+target_dict[key])

        print(dict_tmp)
        print('#####################')
        site_name = []
        site_score = []
        for i in dict_tmp.items():     # 將景點和評論提取出來
            # print(i)     # 為tuple形式
            print(i[0])     # 景點
            # print(i[1])     # 評論
            snow_comment = SnowNLP(i[1])
            score = 0     # 用以分數總合計算
            for n, s in enumerate(snow_comment.sentences) :     # 提取評論斷句，n用以計算index數
                # print(s)
                snow = SnowNLP(s)     #
                point = snow.sentiments
                # print(point)     # 每個斷句情緒分數
                score += point     # 分數總合
            # print(n+1)     # 顯示分成幾句
            grade = score/(n+1)     # 整個景點情緒分數
            print('分數: ', grade)
            # nlp = SnowNLP(i[1])
            # grade = nlp.sentiments
            # print(grade)
            print('========================================================')
            site_name.append(i[0])

            site_score.append(grade)

        # print(site_name)
        # print(site_score)
        new_dict = dict(zip(site_name, site_score))
        print(new_dict)     # 以字典形式顯示景點、情緒分數
        # ----- 以json檔存取 -----
        json_dict = json.dumps(new_dict, ensure_ascii=False)
        with open(r'./score/%s/台北%s.json'%(key, key), 'w', encoding='utf-8') as file :
            file.write(json_dict)

    '''
    {'地點1':'分數','地點2':'分數','地點3':'分數'}
    '''





if __name__ == '__main__':
    time_start = time.time()
    main()
    cost_time = time.time() - time_start
    print(cost_time / 3600, '小時')
    print('Complete!!!!!!!!!!')