# 京东全网爬虫

## 需求

- 抓取首页的分类信息
  - 大分类的url
  - 中分类的url
  - 小分类的url
- 抓取商品信息
  - 商品名称
  - 价格
  - 评论信息
  -  店铺
  - 促销
  - 选项
  - 图片

## 开发环境和技术

- 技术选择：
- 由于全网爬虫，抓取页面非常多，为了提高抓的速度，选择使用`scrapy`框架+`scrapy_redis`分布式组件
- 由于京东全网的数据量达到了亿级，存储又是结构化数据，
- 数据库，选择使用MongoDB；



# 京东全网爬虫的实现步骤

- 采取广度优先策略，我们把类别和商品信息的抓取分开来做

>优点，提高程序的稳定性



- 总体设计

![image-20191120143929099](https://i.ibb.co/FDqW9vd/image-20191120143929099.png)

## 实现步骤
1. 创建爬虫项目
2. 根据需求，定义数据数据模型
3. 实现分类起虫
4. 保存分类信息
5. 实现商品爬虫
6. 保存商品信息
7. 实现随机User-Agent和代理IP下载器中间件，解决IP反爬。



## 创建爬虫项目

`scrapy startproject jingDong`



## 定义数据模型（要抓取的数据）

### 类别数据模型类

- 用于存储类别信息（Category）-字段：

- `b.category_name`：大类别名称。
- `b_category_url`：大类别URL。
- `m_category_name`：中分类名称。
- `m_category_url`：中分类URL。
- `s_category_name`：小分类名称
- `s_category_url`：小分类URL

### 商品数据模型
- 商品数据模型类：用于存储商品信息（Product）字段：
- oproduct_category：商品类别
- product_sku_id：商品ID
- product_name：商品名称
- product_img_url：商品图片URL 
- product_book_info：图书信息，作者，出版社
- product_option：商品选项
- product_shop：商品店铺
- product_comments：商品评论数量
- product_ad：商品促销
- product_price：商品价格

## 商品的分类爬虫

- 创建爬虫
- 进入项目目录：cd mall_spider
- 创建爬虫：scrapy genslider category_spider jd.com
- 指定起始URL
- 修改起始URL: https://dc.3.cn/category/get

## 实现保存分类的pipeline类

- open_spider 方法中，链接MongoDB数据库，获取要操作的集合
- process_item 方法中，向MongoDB中插入类别数据
- close_spider 方法中，关闭MongoDB的链接



# 实现商品爬虫

- 步骤
  - 分析，确定数据所在的URL 
  - 代码实现（核心）
  - 商品爬虫实现分布式
- 分析，确定数据所在的URL 
  - 解析列表页，提取商品sku_id，实现翻页，确定翻页的URL 
  - 获取商品的基本信息，通过手机抓包（APP），确定URL
  - PC详情页面，确定商品的促销信息的URL 
  - PC详情页面，确定评论信息的URL 
  - PC详情页面，确定商品价格信息的URL



- 代码实现

- 1.重写start_requests方法，根据分类信息构建列表页的请求

- 2.解析列表页，提取商品的skuid，构建商品基本的信息请求；实现列表翻页

  1.确定商品基本的信息请求

  1.URL:https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/32962088964.json
  2.请求方法：GET
  3.参数/数据：32962088964商品的skuid
  2.解析列表页，提取商品的skuid
  3.构建商品基本的信息请求
  4.实现列表翻页

- 解析促销信息，构建商品评价信息的请求

- 1.解析促销信息

  - 1.produft_ad：商品促销

  - 2.构建商品评价信息的请求
    -  1.准备评价信息的请求
  
- 解析商品评价信息，构建价格信息的请求

- 解析商品评价信息

  - 1.product_comments：商品评论数量
  - 2.评价数量，好评数量，差拜数量，好评率
  - 2.构建价格信息的请求

- 准备价格请求：

  - 1.URL:https://p.3.cn/prices/mgets?skulds=J_69334292.
  - 2.请求方法：GET
  - 3.参数：skulds=J_6933429，j后跟这个商品的sku_id

- 解析价格信息

  - 1.product_price：商品价格
  - 2.把商品数据交给引擎

# 商品爬虫实现分布式
- 修改爬虫类
  - 修改继承关系
  - 指定redis_key
  - 把重写start_requests改为重写make_request from data I 
- 在settings文件中配置scrapy_redis
  - 直接拷贝scrapy_redis配置信息，到settings.py中.
- 写一个程序用于把MongoDB中分类信息，放入到爬虫redis_key指定的列表中

# 保存商品数据
- 实现存储商品Pipeline类
  - 在open_spider方法，建立MongoDB数据库连接，获取要操作的集合
  - 在process_item方法，把数据插入到MongoDB中
  - 在close_spider方法，关闭数据库连接
- 在settings.py中开启这个管道

# 实现下载器中间件
- 实现随机User-Agent的中间件

- 在settings.py中开启上面的下载器中间
  件