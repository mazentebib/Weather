import requests
import argparse
import pandas as pd
from flatten_json import flatten

def get_data(key, city, day):
    url = "http://api.weatherapi.com/v1/history.json?key={}&q={}&dt={}".format(key,city,day)
    response = requests.get(url)
    api_data = response.json()
    data = pd.json_normalize(api_data,  record_path=['forecast', 'forecastday', 'hour'], meta=["location",
                                                                                                        ['forecast','forecastday','date']])
    df = pd.DataFrame([flatten(x) for x in data['location']])
    data = data.drop('location', axis=1)
    df_concat = pd.concat([df,data],axis = 1)
    df_concat.to_csv('file.csv',mode='a', index = False, encoding='utf-8',header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get historic data')
    parser.add_argument('--key', type=str,
                    help='api key')

    parser.add_argument('--city', type=str,help='city')

    parser.add_argument('--day', type=str,
                        help='data (max 14days earlier from today)')
    args = parser.parse_args()
    get_data(args.key,args.city,args.day)
