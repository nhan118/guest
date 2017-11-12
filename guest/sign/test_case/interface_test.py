import requests
import unittest

class GetEvnetListTest(unittest.TestCase):
    '''查询发布会接口测试'''
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    def test_get_event_null(self):
        '''发布会id为空'''
        r = requests.get(self.url, params={'eid':''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        '''发布会id不存在'''
        r = requests.get(self.url, params={'eid': '901'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_success(self):
        '''发布会id为1，查询成功'''
        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '三星Note8发布会')
        self.assertEqual(result['data']['address'], '北京三星大厦')
        self.assertEqual(result['data']['start_time'], '2017-11-11T10:00:00')

if __name__ == '__main__':
    unittest.main()

# 查询发布会接口
# url = 'http://127.0.0.1:8000/api/get_event_list/'
# r = requests.get(url, params={'eid':'1'})
# result = r.json()

# 断言接口返回值
# assert result['status'] == 200
# assert result['message'] == 'success'
# assert result['data']['name'] == '三星NOTE8发布会'
# assert result['data']['address'] == '北京三星大厦'
# assert result['data']['start_time'] == '2017-11-11T10:00:00'
