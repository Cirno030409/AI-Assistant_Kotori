import pprint

#インターネット上からデータを取得するためのモジュールをインポート
import requests
#リクエストするURLを指定(最新の地震情報のデータを取得することができるURL)
p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=556&limit=5'
#リクエスト(データを取得する)
p2pquake_json = requests.get(p2pquake_url).json()

pprint.pprint(p2pquake_json)


