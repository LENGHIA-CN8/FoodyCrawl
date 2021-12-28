import scrapy
import json
import csv
from ..items import FoodyItem


OUTPUT_DIRECTORY =  "/Users/user/Desktop/Crawl/foody/OUTPUT/foody_output.json"

class CrawlfoodySpider(scrapy.Spider):
    name = 'crawlFoody'
    allowed_domains = ['www.foody.vn']
    total_comment = 0
    num_of_page = 1
    url = 'https://www.foody.vn/__get/Place/HomeListPlace?t=1631867059243&page={}&lat=10.823099&lon=106.629664&count=12&districtId=21&cateId=&cuisineId=&isReputation=&type=1'

    def start_requests(self):
        yield scrapy.Request(self.url.format(self.num_of_page),callback=self.parse)

    def parse(self, response):
        if response.status == 200 and self.total_comment <= 4000:
            res = response.json()
            for i in res['Items']:
                item = {'ResId': i['Id'], 'ResName': i['Name']}
                if i['Url'] is not None:
                    yield scrapy.Request(url='https://www.foody.vn'+i['Url'], callback=self.parse_res, meta={'item': item})

    def parse_res(self,response):
        item = response.meta.get('item')
        resid = item['ResId']
        url = 'https://www.foody.vn/__get/Review/ResLoadMore?t=1632416315325&Type=1&fromOwner=&isLatest=true&ExcludeIds=&ResId=' + str(
            resid) + '&Count=20'
        score = response.css('div.microsite-top-points span ::text').getall()
        resinfo = {
            'ResId': item['ResId'],
            'ResName': item['ResName'],
            'streetAddress': response.css('span[itemprop="streetAddress"] ::text').get(),
            'district': response.css('span[itemprop="addressLocality"] ::text').get(),
            'region': response.css('span[itemprop="addressRegion"] ::text').get(),
            'Res_rating': response.css('div[itemprop="ratingValue"] ::text').get().strip("\r\n "),
            'Res_pos_score': score[0],
            'Res_price_score': score[1],
            'Res_food_score': score[2],
            'Res_atmosphere_score': score[3],
            'Res_services_score': score[4],
        }
        # print(response.css('div.res-common-info  div.disableSection span[itemprop="streetAddress"] ::text').get())
        yield scrapy.Request(url, callback=self.parse_comment,meta={'item':resinfo})

    def parse_comment(self, response):
        reviews = response.json()
        # print(len(reviews))
        meta1 = response.meta.get('item')
        print('_____LEN______',len(reviews['Items']))
        for review in reviews['Items']:
            if len(review['Pictures']) > 0:
                self.total_comment += 1
                item = {
                    # 'ResId': response.meta.get('ResId'),
                    'RevId': review['Id'],
                    'UserId': review['Owner']['Id'],
                    'UserName': review['Owner']['DisplayName'],
                    'Rating': review['AvgRating'],
                    'Comment': review['Description'],
                    'image_urls': [picture['Url'] for picture in review['Pictures']]
                }
                item.update(meta1)
                url = 'https://www.foody.vn/__get/Review/GetReviewInfo?reviewId={}'
                # print(review.css('div.review-user a::attr(data-user)').get())
                yield scrapy.Request(url.format(item['RevId']) ,callback=self.parse_comment_score, meta={'item': item})
            # print(item)
        print('------Total----', self.total_comment)
        self.num_of_page += 1
        # if self.num_of_page <= 10:
        if self.num_of_page < 100:
            yield scrapy.Request(self.url.format(self.num_of_page),callback=self.parse)

    def parse_comment_score(self,response):
        item = response.meta.get('item')
        comment_attr = response.json()
        item2 = {
            'Food_score_cmt': comment_attr['Food'],
            'Services_score_cmt': comment_attr['Services'],
            'Atmosphere_score_cmt': comment_attr['Atmosphere'],
            'Position_score_cmt': comment_attr['Position'],
            'Price_score_cmt': comment_attr['Price']
        }
        item.update(item2)
        url = 'https://www.foody.vn/__get/Review/GetUserInfoReview?userId={}'
        yield scrapy.Request(url.format(item['UserId']),callback=self.parse_user_info, meta={'item': item})
    def parse_user_info(self,response):
        item = response.meta.get('item')
        user_info = response.json()
        item3 = {
            'Total_reviews': user_info['TotalReviews'],
            'Followers': user_info['TotalFollowers']
        }
        item.update(item3)
        # food_item = FoodyItem()
        # for key in item:
        #     food_item[key] = item[key]
        yield item

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time - start_time)
