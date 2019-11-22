# -*- coding: utf-8 -*-
import scrapy
import json
from jingDong.items import Category


class JdCategorySpider(scrapy.Spider):
    name = 'jd_category'
    allowed_domains = ['3.cn']
    start_urls = ['https://dc.3.cn/category/get']

    def parse(self, response):

        result = json.loads(response.body.decode('GBK'))
        datas = result['data']
        # print(datas)
        # 遍历数据列表
        for data in datas:

            item = Category()

            b_category = data['s'][0]
            b_category_info = b_category['n']
            # print("大分类：{}".format(b_category_info))
            item['b_category_name'], item['b_category_url'] = self.get_category_name_url(b_category_info)

            # 中分类信息的列表
            m_category_s = b_category['s']
            # 遍历下分类列表
            for m_category in m_category_s:
                # 中分类信息
                m_category_info = m_category['n']
                # print("中分类：{}".format(m_category_info))
                item['m_category_name'], item['m_category_url'] = self.get_category_name_url(m_category_info)
                # 小分类数据列表
                s_category_s = m_category['s']
                for s_category in s_category_s:
                    s_category_info = s_category['n']
                    # print("小分类：{}".format(s_category_info))
                    item['s_category_name'], item['s_category_url'] = self.get_category_name_url(s_category_info)
                    yield item

    def get_category_name_url(self, category_info):
        """
        根据分类的信息，提取名称和url
        :param category_info: 分类xinx
        :return: 分类的名称和url
        """
        categorys = category_info.split('|')
        # 分类的URL
        category_url = categorys[0]
        # 分类的名称
        category_name = categorys[1]

        # 处理第一类URL
        if category_url.count('jd.com') == 1:
            # 补全URL
            category_url = 'https://' + category_url
        # 处理第二类URL
        elif category_url.count('-') == 1:
            'https://channel.jd.com/{}.html'.format(category_url)
        # 处理第三类URL
        else:
            category_url = category_url.replace('-', ',')
            category_url = 'https://list.jd.com/list.html?cat={}'.format(category_url)

        # 返回类别的名称和URL
        return category_name, category_url


