#!/usr/bin/env python
#coding:utf-8
 
import sys
import urllib
import json
 
def yapi_topics():
    url = 'http://shopping.yahooapis.jp/ShoppingWebService/V1/json/queryRanking?'
    appid = 'YPX'
    params = urllib.urlencode(
                    {'appid': appid,
                     'hits': 50,
                    })
     
    response = urllib.urlopen(url+params)
    return response.read()
 
def do_json(s):
    data = json.loads(s)
    #print(json.dumps(data, sort_keys=True, indent=4)); sys.exit()
     
    item_list = data["ResultSet"]["0"]["Result"]
    #print(json.dumps(item_list, sort_keys=True, indent=4))
    #print item_list.keys()
 
    ranking = {}
    for k, v in item_list.iteritems():
        try:
            rank = int(v["_attributes"]["rank"])
            vector = v["_attributes"]["vector"]
            query = v["Query"]
            ranking[rank] = [vector, query]
        except:
            if k == "RankingInfo":
                StartDate = v["StartDate"]
                EndDate = v["EndDate"]
 
 
    print u"集計開始日:", StartDate
    print u"集計終了日:", EndDate
    print '-' * 40
    ranking_keys = list(ranking.keys())
    ranking_keys.sort()
    #ranking_keys.reverse() /* 降順に表示する */
    for i in ranking_keys:
        print i, ranking[i][0], ranking[i][1]
 
if __name__ == '__main__':
    json_str = yapi_topics()
    do_json(json_str)
