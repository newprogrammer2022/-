from datetime import datetime, timezone
import urllib.parse
import pytz
import requests
import sys
import numpy as np


class BaiDuIndex():
    def __init__(self):
        self.headers = {'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'Cipher-Text': '1704366501069_1704436341499_XtVsPt5lfoWBEL0xky+ghPYfMb/3mIa7O313gHT7lDvs+YUSgToXVhuqAjGbVN/GxbgoGziEA8fEL+F2OAcRXkshyJxeXKklQdx8Pbs1a3Z17U2IQpbKxdJVv5Z6QaI+4bawz0EU2R0O+gQAgjgPYQLMOVls1z8uF4ZK9CZsiEQcznGRVYhmFqsHP9oBkSMxq+QK5hxD1NuOmicmi11sUZMmmc3OWFah3J4KVKcjB9lefJoKiZCk2+axcFem1BMOgQJR3UPqCa46WcsipP3UkguZgJKoTCxmqi7qvjgc2KU5EbMyTkCZf1Fg7RhTkNxut5iVuTMqOU2KYk8uneMrAYX4gIJaXTyLO/CoNbIzbfAHKM/Av18KzLTS0bE022IHbS/+/+PXxi/72iEUUbg5gw==',
                        'Connection': 'keep-alive',
                        'Cookie': 'BAIDUID=EDF654C29998888A064504F8C2DB5873:FG=1; BAIDUID_BFESS=EDF654C29998888A064504F8C2DB5873:FG=1; __bid_n=18a49298de387369e2ad72; BDUSS=TIzOXRvbGdvQW1OLWlBT04wZVcyeXRzQXg3bkYzekFzNkk0dThhanJvTFZueGRsSVFBQUFBJCQAAAAAAAAAAAEAAADc5nHEa2tra2tra2trZ2dnZ2gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANUS8GTVEvBkd; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1703745861; BCLID=7018796594668026993; BCLID_BFESS=7018796594668026993; BDSFRCVID=oJuOJeC62lNvwtjquz4yupjJqKzs_DQTH6_nLvV65JTQZf_Dv4yVEG0PgU8g0K4b6jXGogKK0eOTHkCF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; BDSFRCVID_BFESS=oJuOJeC62lNvwtjquz4yupjJqKzs_DQTH6_nLvV65JTQZf_Dv4yVEG0PgU8g0K4b6jXGogKK0eOTHkCF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF=tbC8VCDatCL3fn5kMn__-4_tbh_X5-RLf54Oal7F5l8-hRR85RJMMR_lhHry-ROBWj6iXtO73UjxOKQ3hxv-3650yROIXt5d3TFJXxQN3KJmeUK9bT3vj-jBMR7x2-biWbR-2Mbd2hOP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJh-PGe6_KDjQbjH_8q-J3K6PX3RTEa-Osfjrn-TRxjn0gyxomtjjxHm60bC5hyqDVj-5xMx6aDnLUjMJILUkqXKoj-h5wbJToEpQD5hOdMb3yQttjQP3PfIkjahQSa-okEn7TyU42bf47yMRm0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OOJRLeoCIXtCKaMCv6btTO5DCV-frb-C62aKDsWhcaBhcqEIL4hMT-5n0qKqoEtnct-IQZQlvL-M7UVfbSjln_XbKZjGoZLpoz5HORLDbXQq5nhMJT3j7JDMn3-GjBXUby523ion5vQpnOEpQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0x25_0-nDSHHLJt5k83j; H_BDCLCKID_SF_BFESS=tbC8VCDatCL3fn5kMn__-4_tbh_X5-RLf54Oal7F5l8-hRR85RJMMR_lhHry-ROBWj6iXtO73UjxOKQ3hxv-3650yROIXt5d3TFJXxQN3KJmeUK9bT3vj-jBMR7x2-biWbR-2Mbd2hOP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJh-PGe6_KDjQbjH_8q-J3K6PX3RTEa-Osfjrn-TRxjn0gyxomtjjxHm60bC5hyqDVj-5xMx6aDnLUjMJILUkqXKoj-h5wbJToEpQD5hOdMb3yQttjQP3PfIkjahQSa-okEn7TyU42bf47yMRm0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OOJRLeoCIXtCKaMCv6btTO5DCV-frb-C62aKDsWhcaBhcqEIL4hMT-5n0qKqoEtnct-IQZQlvL-M7UVfbSjln_XbKZjGoZLpoz5HORLDbXQq5nhMJT3j7JDMn3-GjBXUby523ion5vQpnOEpQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0x25_0-nDSHHLJt5k83j; bdindexid=8b2e7lramaj0gnnjsqll7k7ea4; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a045443357558GfagbthuHxZmRAwru%2Bk7%2Fr7xAsVo%2BJWlclVshKSW32%2FQnn7QoTBJiUSmTqrBa7Pb%2FNP6F4Yq5J4lQAz10PSEp%2BbJ0tlluqCTly3SUmPUAp9%2Fa9LRAz72BfXaC8g7%2Fx6imTikG6rmKrB5pTBEvqzm1t%2F381M7DJbImw3kxFa%2FMIqYLgdR2%2BAD%2B2xM%2BZ3Y0IIwvJn%2FcnFs4ZdN%2BQuRll1PkP8zuOyuQZPFz4YpzIJmNN4ReAognT%2Bjm8mSUByGjBLMDTUeLm%2FKaRuhN%2BbkUgMKfOIXyXSYat1dyx3g7kEhEI%3D67889784785357196614586514829634; __cas__rn__=454433575; __cas__st__212=4671b9429585c4a58e70ba701044eefd9658227eab1f2f58aed9b391dbf9933557d01025cb17f01caf786c69; __cas__id__212=52423407; CPTK_212=1346680061; CPID_212=52423407; RT="z=1&dm=baidu.com&si=1076f445-985e-4196-8b5c-f029cade7c47&ss=lr0965g3&sl=3&tt=47i&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1704436341; BDUSS_BFESS=TIzOXRvbGdvQW1OLWlBT04wZVcyeXRzQXg3bkYzekFzNkk0dThhanJvTFZueGRsSVFBQUFBJCQAAAAAAAAAAAEAAADc5nHEa2tra2tra2trZ2dnZ2gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANUS8GTVEvBkd; ab_sr=1.0.1_MTY2NjYxNGFhZjMyNDY3MDliNGE1NWI0NGJlMTc5NDUxNDcxYzJkYjlhN2VmMmUwZjgxM2YzZTQyZDJjYjYxYTM2ZmJjODNmN2I1MmEzYjYyNTBkYWI3ZGRkZmFhOWU5MDU0YTRmNmRiYWU1NWQ1YWYxNzkyOTljYWFhZjMzOWQ5OWJlMDFjMDc0M2YzMGViYTc2YjZmNjE4MWQxZGM3Mg==',
                        'Host': 'index.baidu.com',
                        'Referer': 'https://index.baidu.com/v2/main/index.html',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                        'sec-ch-ua': "'Not_A Brand';v='8', 'Chromium';v='120', 'Microsoft Edge';v='120'",
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': "'Windows'"
                        }

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
