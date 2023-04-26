
import requests
import json
import sys 
import datetime
import schedule
import time
def main():
    #日付情報の取得
    dt_now = datetime.datetime.now()
    Send_date=str(dt_now.year) +'年'+ str(dt_now.month) + '月' +str(dt_now.day) + '日'
    
    # 気象庁データの取得
    jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/015000.json"
    json_file = requests.get(jma_url).json()
    
    # 取得したいデータを選ぶ
    weather_area=json_file[0]['timeSeries'][2]['areas'][0]['area']['name']
    weather = json_file[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    Min_tempureture=json_file[1]['timeSeries'][1]['areas'][0]['tempsMin'][1]
    Max_tempureture=json_file[1]['timeSeries'][1]['areas'][0]['tempsMax'][1]

    #送信するメッセージの作成
    Send_place_weather_Message=weather_area+'の天気'+'\n'+weather 
    Send_temps_Message='最低気温:'+Min_tempureture +'\n'+'最高気温:'+Max_tempureture
    Send_Message='\n'+ Send_date +'\n'+Send_place_weather_Message + '\n' + Send_temps_Message
    # 全角スペースの削除
    weather = weather.replace('　', '')

    #送信するLineの設定
    access_token='6phwMKIHw93GxsEUgMQ97VYyoKjUANlgabYUTaNpqZX'
    url = 'https://notify-api.line.me/api/notify'
    headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }
    #メッセージを送る
    payload = {
            'message': Send_Message ,
        }
    response = requests.post(url, headers=headers, params=payload)
    res = json.loads(response.text)
    
    print('送信しました')
    


#毎日指定した時刻に送信
schedule.every().day.at("06:00").do(main)
#処理の軽減
while True:
    schedule.run_pending()
    time.sleep(1)
