
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import CsvItemExporter
from scrapy import signals

class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[-1]

class FoodyPipeline:
    # def __init__(self):
    #     self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('../OUTPUT/Foody.csv', 'w+b')
        self.file1 = open('../OUTPUT/Restaurant.csv', 'w+b')
        self.file2 = open('../OUTPUT/User.csv', 'w+b')
        self.file3 = open('../OUTPUT/Comment.csv', 'w+b')

        self.exporter = CsvItemExporter(self.file)
        self.exporter1 = CsvItemExporter(self.file1)
        self.exporter2 = CsvItemExporter(self.file2)
        self.exporter3 = CsvItemExporter(self.file3)

        self.exporter1.fields_to_export = ['ResId','Rating','streetAddress','district','region','Res_pos_score','Res_price_score','Res_food_score','Res_atmosphere_score','Res_services_score']
        self.exporter2.fields_to_export = ['UserId','Total_reviews','Followers']
        self.exporter3.fields_to_export = ['RevId','UserId','ResId','Comment','image_urls','Food_score_cmt','Services_score_cmt','Atmosphere_score_cmt','Position_score_cmt','Price_score_cmt' ]

        self.exporter.start_exporting()
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()
        self.exporter3.start_exporting()


    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.exporter1.finish_exporting()
        self.exporter2.finish_exporting()
        self.exporter3.finish_exporting()

        self.file.close()
        self.file1.close()
        self.file2.close()
        self.file3.close()

    def process_item(self, item, spider):
        # print('_________ITEM______\n',item)
        self.exporter.export_item(item)
        self.exporter1.export_item(item)
        self.exporter2.export_item(item)
        self.exporter3.export_item(item)
        return item
