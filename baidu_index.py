from datetime import datetime, timezone
import urllib.parse
import pytz
import requests
import sys
import numpy as np


class BaiDuIndex():
    def __init__(self):
        # 把网页内的请求头贴到这里
        self.headers = {}

    def decrypt(self, t, e):
        # 解密数据
        n = list(t)
        # i = list(e)
        a = {}
        result = []
        ln = int(len(n) / 2)
        start = n[ln:]
        end = n[:ln]
        for j, k in zip(start, end):
            a.update({k: j})
        for j in e:
            result.append(a.get(j))
        return ''.join(result).split(',')

    def get_ptbk(self, uniqid):
        uniqid_url = f'https://index.baidu.com/Interface/ptbk?uniqid={uniqid}'
        resp = requests.get(uniqid_url, headers=self.headers)
        if resp.status_code != 200:
            print('获取uniqid失败')
            sys.exit(1)
        return resp.json().get('data')

    def get_half_years_search_index(self, keyword):
        remake_keyword = '{"name": "%s", "wordType": 1}' % keyword
        encoded_keyword = urllib.parse.quote(remake_keyword)
        ori_url = f'https://index.baidu.com/api/SearchApi/index?area=0&word=[[{encoded_keyword}]]&days=180'
        resp = requests.get(ori_url, headers=self.headers)
        # print(resp.json())
        content = resp.json()
        data = content.get('data')
        uniqid = data.get('uniqid')
        ptbk_code = self.get_ptbk(uniqid)
        # print(ptbk_code)
        user_indexes = data.get('userIndexes')[0]
        all_data = user_indexes.get('all').get('data')
        result = self.decrypt(ptbk_code, all_data)
        start_date = user_indexes.get('all').get('startDate')
        # print(result)
        # print(len(result))
        return np.array(result), start_date
        # result = result.split(',')

    def generate_days_utc(self, date_str):
        day_s = 86400
        days_arr = np.arange(0, 180)
        # print(days_arr)

        # 将字符串转换为日期对象，并设置为UTC时区
        utc_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        # 获取该日期0点的时间戳（以秒为单位）
        utc_timestamp = int(utc_date.timestamp())

        # print(utc_timestamp)
        days_utc = days_arr * day_s + utc_timestamp
        # print(days_utc)
        return days_utc

    def generate_half_year_search_data(self, keyword):
        record_dtype = np.dtype([('UTC', 'int32'), ('Index', 'int32')])
        half_year_result, start_date = self.get_half_years_search_index(keyword)
        date_list = self.generate_days_utc(start_date)
        half_year_data = np.empty(len(half_year_result), dtype=record_dtype)
        # print(half_year_data)
        half_year_data['UTC'] = date_list
        half_year_data['Index'] = half_year_result
        return half_year_data

    def get_feed_data_week(self, keyword):
        remake_keyword = '{"name": "%s", "wordType": 1}' % keyword
        encoded_keyword = urllib.parse.quote(remake_keyword)
        test_url = f'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?area=0&word=[[{encoded_keyword}]]'
        resp = requests.get(test_url, headers=self.headers)
        print(resp.json())
        content = resp.json()
        data = content.get('data')
        uniqid = data.get('uniqid')
        ptbk_code = self.get_ptbk(uniqid)
        print(ptbk_code)
        user_indexes = data.get('index')[0]
        all_data = user_indexes.get('data')
        result = self.decrypt(ptbk_code, all_data)
        print(result)
        # result = result.split(',')

    def get_info_index_data(self, keyword):
        remake_keyword = '{"name": "%s", "wordType": 1}' % keyword
        encoded_keyword = urllib.parse.quote(remake_keyword)
        test_url = f'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?word=[[{encoded_keyword}]]&area=0&days=30'
        resp = requests.get(test_url, headers=self.headers)
        # print(resp.json())
        content = resp.json()
        data = content.get('data')
        uniqid = data.get('uniqid')
        ptbk_code = self.get_ptbk(uniqid)
        # print(ptbk_code)
        user_indexes = data.get('index')[0]
        all_data = user_indexes.get('data')
        result = self.decrypt(ptbk_code, all_data)
        return result

    def get_living_time_index(self, keyword):
        remake_keyword = '{"name": "%s", "wordType": 1}' % keyword
        encoded_keyword = urllib.parse.quote(remake_keyword)
        # 实时数据的url
        test_url = f'https://index.baidu.com/api/LiveApi/getLive?region=0&word=[[{encoded_keyword}]]'
        resp = requests.get(test_url, headers=self.headers)
        # print(resp.json())
        content = resp.json()
        data = content.get('data')
        uniqid = data.get('uniqid')
        # 数据解密需要uniqid
        ptbk_code = self.get_ptbk(uniqid)
        # print(ptbk_code)
        result = data.get('result')[0].get('index')[0]
        # print(result)
        all_data = result.get('_all')
        time_period = result.get('period')
        living_result = self.decrypt(ptbk_code, all_data)
        # print(living_result)
        # print(len(living_result))
        return living_result, time_period

    def generate_last_day_hours(self, date_str):
        start_end = date_str.split('|')
        # print(start_end)

        # 获取本地时区（这里以亚洲/上海为例）
        local_tz = pytz.timezone('Asia/Shanghai')

        # 转换为本地时区的datetime对象并转换为UTC时间戳
        start_timestamp_utc = (
            local_tz.localize(datetime.strptime(start_end[0], '%Y-%m-%d %H:%M:%S')).astimezone(
                timezone.utc)).timestamp()
        day_s = 3600
        days_arr = np.arange(0, 24)
        hours_utc = days_arr * day_s + int(start_timestamp_utc)
        return hours_utc

    def generate_living_data(self, keyword):
        record_dtype = np.dtype([('UTC', int), ('Index', int)])
        living_result, time_period = self.get_living_time_index(keyword)
        date_list = self.generate_last_day_hours(time_period)
        living_data = np.array(list(zip(date_list, living_result)), dtype=record_dtype)
        return living_data


if __name__ == '__main__':
    get_baidu_index = BaiDuIndex()
    living_index = get_baidu_index.generate_living_data('ai')
    print(living_index)
    half_year = get_baidu_index.generate_half_year_search_data('ai')
    print(half_year)
