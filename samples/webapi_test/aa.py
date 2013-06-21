# -*- coding: utf-8 -*-
# Google の Custom Search Engine で画像を検索するサンプル
from apiclient.discovery import build
import pprint

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
                  developerKey="AIzXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") # API Key (39文字)

  res = service.cse().list(
    q=u'スティーブ・ジョブズ',
    searchType='image',
    # imgType='face',
    cx='999999999999999999999:xxxxxxxxxxx', # 検索エンジンID (33文字)
    ).execute()

  #pprint.pprint(res)
  return res

if __name__ == '__main__':
  result = main()

  #import pickle
  #pickle.dump(result, open("result.dump", "w"))

  #src = result['items'][0]['link']
  src = result['items'][0]['image']['thumbnailLink']

  import os
  os.system('open %s' % src)
