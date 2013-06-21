# -*- coding: utf-8 -*-
# Google APIs Client Library for Python
# https://developers.google.com/api-client-library/python/start/get_started

from apiclient.discovery import build
import pprint


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
                  developerKey="AIzaSyCDl5uFdgrcHqbVGBRaQo3p3x5EocEdifU") # API Key

  res = service.cse().list(
    q=u'ガールズ&パンツァー',
    cx = '005780922867090589679:4z9wr2n1i6g', # 検索エンジンID
    ).execute()

  # pprint.pprint(res)
  return res

if __name__ == '__main__':
  result = main()

  import pickle
  pickle.dump(result, open("result.dump", "w"))
