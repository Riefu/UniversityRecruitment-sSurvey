import json
import requests
from jedis import jedis
from util import util


# 添加中央财经大学的数据
def get_cufe_rescruit():
    base_url = "http://scc.cufe.edu.cn/recruitment-datas/15/"
    url_tail = "/2.html"
    host = "scc.cufe.edu.cn"
    req = requests.Session()
    header = jedis.get_header(host)
    re = jedis.jedis()
    re.connect_redis()
    max_page_num = 422
    for i in range(1, max_page_num):
        print(i)
        url = base_url + str(i) + url_tail
        res = req.get(headers=header, url=url).content.decode("utf-8")
        parse_info(res, re)
    re.add_university("cufe_company_info")


def parse_info(res, re):
    json_data = json.loads(res)

    for item in json_data['results']:
        if 'enterprise' in item:
            info = item['enterprise']
            company_name = info['name']
            date = item['startTime']
            date = util.get_standard_date(date)
        else:
            company_name = item['title']
            date = item['publishTime']
        print(date)
        print(company_name)
        re.save_info("cufe_company_info", date, company_name)

if __name__ == '__main__':
    get_cufe_rescruit()

